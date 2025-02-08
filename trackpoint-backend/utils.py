import hashlib
import mimetypes
import secrets
import string
from datetime import datetime, timedelta
from uuid import uuid4
from typing_extensions import TypedDict


import jwt
from fastapi_boot.core import Component

from domain.config import ProjConfig
from exception import BusinessException


@Component
class MD5Util:
    def encrypt(self, data: str):
        md5_hash = hashlib.md5()
        md5_hash.update(data.encode('utf-8'))
        return md5_hash.hexdigest()

    def verify(self, data: str, hashed_value: str):
        return self.encrypt(data) == hashed_value


class Payload(TypedDict):
    """jwt载荷"""
    id: str


@Component
class JWTUtil:

    def __init__(self, config: ProjConfig):
        self.expires = config.jwt.access_tokne_expires
        self.algorithm = config.jwt.algorithm
        self.secret_key = config.jwt.secret_key

    def create(self, data: Payload, expires: int | None = None) -> str:
        """默认使用access_token_expires"""
        expires_ = expires if isinstance(expires, int) else self.expires
        data_ = {**data, 'exp': datetime.now() +
                 timedelta(seconds=expires_)}
        return jwt.encode(data_, self.secret_key, self.algorithm)

    def verify(self, token: str) -> Payload:
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except:
            raise BusinessException(status_code=401, detail='unauthorization')


def gid():
    """生成随机uuid"""
    return str(uuid4())


def gnow():
    """获取当前daetetime"""
    return datetime.now()


def gen_random_verifycode(length: int = 6):
    """
    生成随机六位验证码
    :return: str
    """
    characters = string.ascii_letters + string.digits
    secure_code = ''.join(secrets.choice(characters) for _ in range(length))
    return secure_code


def format_pydantic_datetime(v: datetime) -> str:
    """格式化pydantic模型中的datetime"""
    return v.strftime('%Y-%m-%d %H:%M:%S')


# def get_curr_format_datetime() -> str:
#     """获取当前格式化后的时间"""
#     return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_file_extension(content_type: str) -> str:
    """
    根据content-type获取文件后缀，有.

    :param content_type: 文件的MIME类型
    :return: 文件后缀，如果没有找到对应的后缀则返回空字符串
    """
    return mimetypes.guess_extension(content_type) or ''


def get_media_type_from_filename(filename: str) -> str:
    """
    根据文件名获取MIME类型。

    :param filename: 文件名
    :return: MIME类型，如果没有找到对应的类型则返回 'application/octet-stream'
    """
    media_type, _ = mimetypes.guess_type(filename)
    return media_type or 'application/octet-stream'


# def ensure_list(data: list | dict):
#     """确保参数是列表，用于tortoise的JSONField"""
#     if isinstance(data, dict):
#         raise BusinessException(detail='服务器错误')
#     return data


# def ensure_dict(data: list | dict):
#     """确保参数是字典，用于tortoise的JSONField"""
#     if isinstance(data, list):
#         raise BusinessException(detail='服务器错误')
#     return data
