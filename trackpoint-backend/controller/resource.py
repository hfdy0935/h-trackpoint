from fastapi import HTTPException, Path, Response
from fastapi.responses import FileResponse, StreamingResponse
from fastapi_boot.core import Controller, Get, use_dep
from minio import S3Error

from constants import RESOURCE_PREFIX, RequestConstant
from dependencies import use_session, use_login
from exception import BusinessException
from service.minio import MinIOService
from service.resource import ResourceService
from utils import get_media_type_from_filename


@Controller(f'/{RESOURCE_PREFIX}', tags=['资源'])
class ResourceController:
    user = use_dep(use_login)

    def __init__(self, minio_service: MinIOService, resource_service: ResourceService) -> None:
        self.minio_service = minio_service
        self.resource_service = resource_service

    @Get('/{filename}', summary='获取资源')
    async def get_file(self, filename: str = Path(description='资源路径')):
        # 判断是不是当前用户的图片
        owner = await self.resource_service.get_owner_of_resource(filename)
        if (not owner) or owner.id != self.user.id:
            raise BusinessException(detail='资源不存在或无权查看')
        content = self.minio_service.get(filename)
        media_type = get_media_type_from_filename(filename)
        return StreamingResponse(content=[content], media_type=media_type)
