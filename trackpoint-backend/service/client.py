import os
from typing import Any
from fastapi import UploadFile
from fastapi_boot.core import Service, Inject
from tortoise.transactions import atomic

from constants import RESOURCE_PREFIX
from dao.event import DefaultEventDAO
from domain.config import ProjConfig
from domain.dto.client import ClientRegisterDTO, ClientSendEventsDTO, EventDTO
from domain.entity.bind_param import BindParam
from domain.entity.client import Client
from domain.entity.default_event import DefaultEvent
from domain.entity.eventbind_param import EventBindParam
from domain.entity.project import Project
from domain.entity.record import Record
from domain.entity.custom_event import CustomEvent
from enums import BindParamTypeEnum
from exception import BusinessException
from service.minio import MinIOService
from utils import JWTUtil, MD5Util,  get_file_extension, gid, gnow


def getTypeByDbTypeStr(s: BindParamTypeEnum):
    """根据数据库绑定参数的字段类型返回python类型"""
    if s == BindParamTypeEnum.NUMBER:
        return (int, float)
    elif s == BindParamTypeEnum.ARRAY:
        return (list,)
    elif s == BindParamTypeEnum.OBJECT:
        return (dict,)
    elif s == BindParamTypeEnum.BOOLEAN:
        return (bool,)
    else:
        return (str,)


@Service
class ClientService:
    def __init__(self, jwt: JWTUtil, md5: MD5Util, minio_service: MinIOService, de_dao: DefaultEventDAO) -> None:
        self.jwt = jwt
        self.refresh_token_expires = Inject(
            ProjConfig).jwt.refresh_token_expires
        self.md5 = md5
        self.minio_service = minio_service
        self.de_dao = de_dao

    async def register(self, dto: ClientRegisterDTO, project: Project):
        """客户端注册，简单起见，不用token了，每次请求拿着项目id和项目key验证"""
        # 如果已存在
        if await Client.exists(id=dto.client_id):
            print('客户端已存在')
            return
        # 不存在，新建
        else:
            print('客户端不存在')
            await Client(
                id=dto.client_id,
                os=dto.os.name,
                os_version=dto.os.version,
                browser=dto.browser.name,
                browser_version=dto.browser.version,
                device=dto.device,
            ).save()

    async def verify_params(self, params: dict, event: DefaultEvent | CustomEvent):
        """校验参数，多传没关系，但数据库中要的必须传够

        Args:
            params (dict): 要校验的参数字典
            event (DefaultEvent | CustomEvent): 事件
        """
        # 获取该事件的所有参数
        bind_param_id_list = [i.bind_param_id for i in await EventBindParam.filter(event_id=event.id)]
        bind_param_list = await BindParam.filter(id__in=bind_param_id_list)
        # 只校验必传的
        for bind in bind_param_list:
            if bind.name not in params:
                raise BusinessException(detail=f'事件参数缺少"{bind.name}"')
            bind_type = getTypeByDbTypeStr(bind.type)
            if not isinstance(params.get(bind.name), bind_type):
                raise BusinessException(
                    detail=f'事件参数"{bind.name}"类型错误，应为"{bind.type}"，收到"{type(params.get(bind.name))}"')

    @atomic()
    async def bulk_send_event(self, dto: ClientSendEventsDTO, db_event_list: list[DefaultEvent | CustomEvent], client: Client, screen_shot_path: str) -> list[str]:
        """批量上报事件

        Args:
            dto (ClientSendEventsDTO): 上报事件请求体
            db_event_list (list[DefaultEvent  |  CustomEvent]): 数据库中查到的事件列表
            client (Client): 验证之后的客户端
            screen_shot_path (str): 截图路径，如果之前保存了，这次只需要添加之前的路径

        Returns:
            list[str]: 需要添加截图的记录id列表
        """
        # 返回需要添加截图的记录id
        need_add_shot_list: list[str] = []
        # 批量创建列表
        task_list: list[Record] = []
        db_event_dict = {i.name: i for i in db_event_list}
        # 校验参数及入库
        for event in dto.events:
            db_event = db_event_dict[event.event_name]
            await self.verify_params(event.params, db_event)
            record_id = gid()
            task_list.append(Record(
                id=record_id,
                project_id=dto.project_id,
                event_id=db_event.id,
                client_id=client.id,
                create_time=event.create_time,
                page_url=event.page_url,
                screen_shot_path=screen_shot_path if isinstance(
                    db_event, DefaultEvent) and db_event.need_shot else '',  # 默认事件且需要保存截图
                params=event.params
            ))
            if isinstance(db_event, DefaultEvent) and db_event.need_shot:
                need_add_shot_list.append(record_id)
        await Record.bulk_create(task_list)
        return need_add_shot_list

    @atomic()
    async def upload_screen_shot(self, record_list: list[Record], de: DefaultEvent, file: UploadFile) -> list[str]:
        """上传截图到minio，添加记录到截图表，修改record表，返回截图id列表

        Args:
            record_list (list[Record]): 要把截图添加到哪些上报记录
            de (DefaultEvent): 要添加截图的默认事件，目前只有点击
            file (UploadFile): 截图文件

        Raises:
            BusinessException: 上传失败，上传文件不能为空
            BusinessException: 上传失败，请联系管理员

        Returns:
            list[str]: 截图id列表
        """
        if file.content_type is None or file.size is None:
            raise BusinessException(detail='上传失败，上传文件不能为空')
        sid_list: list[str] = []
        for record in record_list:
            if not isinstance(record.params, dict):
                raise BusinessException(detail='上传失败，请联系管理员')
            # 截图的id，根据参数生成，不用uuid
            sid, filename, path = self.get_shot_paths(
                record.params, de.id, record.page_url)
            if sid not in sid_list:
                sid_list.append(sid)
                self.minio_service.upload(
                    file, file.size, filename)
            record.screen_shot_path = path
        await Record.bulk_update(record_list, fields=['screen_shot_path'])
        return sid_list

    def get_shot_paths(self, params: dict, event_id: str, page_url: str):
        """生成截图id、文件名、minio的存储路径"""
        sid = self.md5.encrypt(
            f"{params.get('w')}_{params.get('h')}_{event_id}_{page_url}")
        filename = sid+'.png'
        path = os.path.join(RESOURCE_PREFIX, filename)
        return sid, filename, path
