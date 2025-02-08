from fastapi import Path
from fastapi.responses import StreamingResponse
from fastapi_boot.core import Controller, Get, use_dep

from constants import RESOURCE_PREFIX, RequestConstant
from dependencies import use_session, use_login
from exception import BusinessException
from service.minio import MinIOService
from service.resource import ResourceService
from utils import get_media_type_from_filename


@Controller(f'/{RESOURCE_PREFIX}', tags=['资源'])
class ResourceController:
    session = use_dep(use_session)

    def __init__(self, minio_service: MinIOService, resource_service: ResourceService) -> None:
        self.minio_service = minio_service
        self.resource_service = resource_service

    @Get('/{filename}', summary='获取资源')
    async def get_file(self, filename: str = Path(description='资源路径')):
        # 判断是不是当前用户的图片
        owner = await self.resource_service.get_owner_of_resource(filename)
        curr_user = await use_login(self.session.get(RequestConstant.User.JWT_SESSION_KEY, ''))
        if (not owner) or owner.id != curr_user.id:
            raise BusinessException(detail='无权查看资源')
        content = self.minio_service.get(filename)
        media_type = get_media_type_from_filename(filename)
        return StreamingResponse([content], media_type=media_type)
