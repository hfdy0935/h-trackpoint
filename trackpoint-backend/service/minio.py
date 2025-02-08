from uuid import uuid4
from fastapi import UploadFile
from fastapi_boot.core import Service
from minio import Minio, S3Error

from domain.config import ProjConfig
from exception import BusinessException


@Service
class MinIOService:
    def __init__(self, minio: Minio, cfg: ProjConfig) -> None:
        self.minio = minio
        self.bucket = cfg.minio.bucket

    def upload(self, file: UploadFile, size: int, filename: str):
        """上传文件

        Args:
            file (UploadFile): _description_
            size (int): _description_
            filename (str): _description_
        """
        try:
            self.minio.put_object(self.bucket, filename, file.file,
                                  size, content_type=file.content_type or 'application/octet-stream')
        except S3Error as e:
            print(e)
            raise BusinessException(detail='上传失败')

    def get(self, filename: str) -> bytes:
        return self.minio.get_object(self.bucket, filename).data
