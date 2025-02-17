
from fastapi import Header, Request
from fastapi_boot.core import Inject

from constants import RequestConstant
from enums import StatusEnum
from exception import BusinessException
from utils import JWTUtil


jwt = Inject(JWTUtil)


async def use_login(token: str = Header(alias=RequestConstant.User.JWT_HEADER_KEY, default='')):
    """获取用户，必须登录"""
    from domain.entity.user import User
    if not token:
        raise BusinessException(status_code=401, detail='Unauthorization')
    user_id = jwt.verify(token)['id']
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise BusinessException(detail='用户不存在')
    if user.status == StatusEnum.DISABLED:
        raise BusinessException(detail='该账号已被封禁，请联系管理员')
    return user


def use_token(token: str = Header(alias=RequestConstant.User.JWT_HEADER_KEY)):
    return token


async def use_session(request: Request):
    return request.session
