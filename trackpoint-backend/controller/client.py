from typing import Annotated
from fastapi import Form, HTTPException,  UploadFile
from fastapi_boot.core import Controller,  Post

from constants import CacheConstant, RequestConstant
from dao.event import CustomEventDAO, DefaultEventDAO
from domain.dto.client import ClientRegisterDTO, ClientSendEventsDTO
from domain.entity.default_event import DefaultEvent
from domain.entity.project import Project
from domain.entity.client import Client
from domain.entity.record import Record
from domain.vo.client import SendEventVO
from domain.vo.common import BaseResp
from enums import StatusEnum
from exception import BusinessException
from helper import HBF
from service.client import ClientService
from service.minio import MinIOService
from utils import JWTUtil, MD5Util
from typing import List



@Controller('/v1/client',tags=['客户端注册上报'])
class ClientController:
    def __init__(self, jwt: JWTUtil, bf: Annotated[HBF, CacheConstant.SCREENSHOT_BF_NAME], client_service: ClientService,
                 minio_service: MinIOService, md5: MD5Util, ce_dao: CustomEventDAO,
                 de_dao: DefaultEventDAO):
        self.jwt = jwt
        self.client_service = client_service
        self.minio_service = minio_service
        self.md5 = md5
        # 布隆过滤器
        self.bf = bf
        self.ce_dao = ce_dao
        self.de_dao = de_dao

    @Post('/register', summary='客户端注册，初始化', response_model=BaseResp[list[str]])
    async def register(self, dto: ClientRegisterDTO):
        project = await Project.get_or_none(id=dto.project_id)
        if project is None:
            raise HTTPException(status_code=404, detail='注册失败，项目不存在')
        if project.status == StatusEnum.DISABLED:
            raise HTTPException(status_code=404, detail='注册失败，项目未启用')
        if self.md5.encrypt(dto.key) != project.key:
            raise HTTPException(status_code=404, detail='注册失败，项目key错误')
        await self.client_service.register(dto, project)
        # 获取默认事件名列表，用于启动自动上报
        data = [i.name for i in await self.de_dao.getEventNameListByProjIdList([project.id])]
        return BaseResp.ok(msg='注册成功', data=data)
    
    @Post('/send-events', summary='上报事件', response_model=BaseResp[List[SendEventVO]])
    async def send_events(self, dto: ClientSendEventsDTO):
        response_list = []  # 用于存储每个事件的返回结果
        pid = dto.project_id
        # 确保项目存在、key正确、状态正常
        project = await Project.get_or_none(pid)
        if project is None:
            raise BusinessException(detail='上报失败，项目不存在')
        if project.status == StatusEnum.DISABLED:
            raise BusinessException(detail='上报失败，项目未启用')
        if self.md5.encrypt(dto.key) != project.key:
            raise BusinessException(detail='上报失败，项目key错误')

        for event in dto.events:  # 遍历事件列表
            # 根据实际名查询该项目下的事件
            db_event = await self.de_dao.getByEventNameAndProjId(event.event_name, project.id) \
                or await self.ce_dao.getByEventNameAndProjId(event.event_name, project.id)

            if db_event is None:
                raise BusinessException(
                    detail=f'上报失败，事件"{event.event_name}"不存在或未启用或不属于当前项目')

            client = await Client.get_or_none(id=dto.client_id)
            if client is None:
                raise BusinessException(detail='上报失败，请先注册项目')

            need_upload_shot = False
            screenshot_path: str = ''

            # 如果默认事件且需要截图
            if isinstance(db_event, DefaultEvent) and db_event.need_shot:
                # 截图id，由浏览器宽高、事件id、页面url组成
                sid = self.md5.encrypt(
                    f"{event.params.get('w')}_{event.params.get('h')}_{db_event.id}_{event.page_url}")
                if not self.bf.exists(sid):
                    need_upload_shot = True
                else:
                    r = await Record.filter(client_id=client.id).first()
                    screenshot_path = r.screen_shot_path if r else ''

            # 上报事件
            record_id = await self.client_service.send_event(event, pid, db_event, client, screenshot_path)
            response_list.append(SendEventVO(
                record_id=record_id,
                need_upload_shot=need_upload_shot
            ))

        return BaseResp.ok(msg='上报成功', data=response_list)    

    @Post('/upload-shot', summary='上传document.body截图', response_model=BaseResp[None])
    async def upload_shot(self, record_id: Annotated[str, Form(description='记录id')], screenshot: Annotated[UploadFile, Form(description='截图')]):
        record = await Record.get_or_none(id=record_id)
        if record is None:
            raise BusinessException(detail='截图上传失败，事件记录不存在')
        # 目前只有默认事件才有截图
        de = await DefaultEvent.get_or_none(id=record.event_id, status=StatusEnum.NORMAL)
        if de is None:
            raise BusinessException(detail='上传失败，事件不存在')
        # 最好再判断一下该record的event的project的id是project_id，这里先不判断了，后面再说
        sid = await self.client_service.upload_screen_shot(de, record, screenshot)
        # 添加到布隆过滤器
        self.bf.add(sid)
        return BaseResp.ok(msg='上传成功')
