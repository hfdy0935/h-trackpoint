from types import NoneType
from typing import Annotated
from fastapi import BackgroundTasks, Form, HTTPException,  UploadFile
from fastapi_boot.core import Controller,  Post


from constants import CacheConstant
from dao.event import CustomEventDAO, DefaultEventDAO
from domain.dto.client import ClientRegisterDTO, ClientSendEventsDTO
from domain.entity.default_event import DefaultEvent
from domain.entity.custom_event import CustomEvent
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


@Controller('/v1/client', tags=['客户端注册上报'])
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
        return BaseResp[list[str]].ok(msg='注册成功', data=data)

    @Post('/send-events', summary='上报事件', response_model=BaseResp[SendEventVO])
    async def send_events(self, dto: ClientSendEventsDTO, bgTask: BackgroundTasks):
        pid = dto.projectId
        # 1. 确保项目存在、key正确、状态正常
        project = await Project.get_or_none(id=pid)
        if project is None:
            raise BusinessException(detail='上报失败，项目不存在')
        if project.status == StatusEnum.DISABLED:
            raise BusinessException(detail='上报失败，项目未启用')
        if self.md5.encrypt(dto.projectKey) != project.key:
            raise BusinessException(detail='上报失败，项目key错误')
        # 2. 确保已注册
        client = await Client.get_or_none(id=dto.uid)
        if client is None:
            raise BusinessException(detail='上报失败，请先注册项目')
        # 3. 确保上报的事件都是该项目下的
        event_name_list = list(set([i.eventName for i in dto.events]))
        db_event_list: list[CustomEvent | DefaultEvent] = (await self.de_dao.getByEventNameListAndProjId(event_name_list, project.id)) +\
            await self.ce_dao.getByEventNameListAndProjId(event_name_list, project.id)
        if len(event_name_list) != len(db_event_list):
            raise BusinessException(detail='上报失败，事件不存在或未启用或不属于当前项目')
        need_upload_shot = False
        screenshot_path = ''  # 如果有截图，需要存到事件记录中
        # 需要截图的事件，即点击事件
        need_upload_event_list = [i for i in db_event_list if isinstance(
            i, DefaultEvent) and i.need_shot]
        if need_upload_event_list:
            db_event = need_upload_event_list[0]
            send_event = [
                i for i in dto.events if i.eventName == db_event.name][0]
            sid, _, path = self.client_service.get_shot_paths(
                send_event.params, db_event.id, send_event.pageUrl)
            screenshot_path = path
            if not self.bf.exists(sid):
                need_upload_shot = True
        # 如果不需要截图，添加到后台任务（大多数事件）
        if not need_upload_shot:
            bgTask.add_task(self.client_service.bulk_send_event,
                            dto, db_event_list, client.id, screenshot_path, False)
            return BaseResp[SendEventVO].ok(msg='提交成功', data=SendEventVO(
                record_id_list=[],
                need_upload_shot=False
            ))
            # 上报事件
        record_id_list = await self.client_service.bulk_send_event(dto, db_event_list, client.id, screenshot_path)
        return BaseResp[SendEventVO].ok(msg='上报成功', data=SendEventVO(
            record_id_list=record_id_list,
            need_upload_shot=need_upload_shot
        ))

    @Post('/upload-shot', summary='上传document.body截图', response_model=BaseResp[NoneType])
    async def upload_shot(self, record_id_list: Annotated[list[str], Form(description='记录id列表')], screenshot: Annotated[UploadFile, Form(description='截图')]):
        record_list = await Record.filter(id__in=record_id_list)
        if len(record_list) != len(record_id_list):
            raise BusinessException(detail='截图上传失败，有事件记录不存在')
        # 目前只有默认事件才有截图
        de = await DefaultEvent.filter(id__in=[i.event_id for i in record_list]).first()
        if de is None:
            raise BusinessException(detail='截图上传失败，该上报记录所属事件不存在')
        sid_list = await self.client_service.upload_screen_shot(record_list, de, screenshot)
        # 添加到布隆过滤器
        self.bf.add(*sid_list)
        return BaseResp[NoneType].ok(msg='上传成功')
