from inspect import isawaitable

from fastapi_boot.core import Controller, Post, use_dep, Inject, Put, Get
from redis import Redis

from domain.entity.user import User
from enums import StatusEnum
from exception import BusinessException
from domain.dto.user import LoginDTO, RegisterDTO, SendEmailCodeDTO, UpdatePasswordByEmailDTO, UpdatePasswordByOriDTO, UpdatePasswordByEmailDTO, UpdateUserInfoDTO
from service.email_service import EmailService
from constants import CacheConstant, RequestConstant
from dependencies import use_session, use_login
from domain.vo.common import BaseResp
from domain.vo.user import LoginVO, RegisterVO, UserVO
from service.user import UserService
from utils import gen_random_verifycode, gid


redis = Inject(Redis)
email_service = Inject(EmailService)
user_service = Inject(UserService)


async def verify_email_code(session: dict, email: str, code: str) -> str:
    """根据session_key合email获取redis中缓存的验证码，并进行验证"""
    # 取出session_id
    session_id: str = session.get(RequestConstant.User.SESSION_ID, '')
    # 查缓存
    key = f'{CacheConstant.EMAIL_CODE}:{email}:{session_id}'
    cache_ = redis.get(key)
    cache: str = await cache_ if isawaitable(cache_) else cache_
    if cache.lower() != code.lower():  # 忽略大小写
        raise BusinessException(detail='验证码错误或已失效，请重新获取')
    return key

PATH = '/v1/user'


@Controller(PATH, tags=['用户登录相关接口'])
class UserController:
    session = use_dep(use_session)

    @Post('/send-email-code', summary='发送邮箱验证码', response_model=BaseResp[None])
    async def send_email_code(self, dto: SendEmailCodeDTO):
        # 如果该邮箱已注册
        if await User.exists(email=dto.email):
            raise BusinessException(detail='发送失败，该邮箱已注册')
        session_id = gid()
        self.session.update({RequestConstant.User.SESSION_ID: session_id})
        # 生成验证码
        code = gen_random_verifycode()
        # 发送邮件
        email_service.send_email_code(dto.email, code)
        # 添加到缓存
        key = f'{CacheConstant.EMAIL_CODE}:{dto.email}:{session_id}'
        redis.set(key, code)
        redis.expire(key, CacheConstant.EXPIRES)
        return BaseResp.ok(msg='发送成功')

    @Post('/register', summary='注册', response_model=BaseResp[RegisterVO])
    async def register(self, dto: RegisterDTO):
        key = await verify_email_code(self.session, dto.email, dto.code)
        if await User.exists(email=dto.email):
            raise BusinessException(detail='注册失败，该邮箱已注册')
        vo = await user_service.register(dto)
        # 清除缓存
        redis.delete(key)
        # session中设置token，以便访问图片
        self.session.update({RequestConstant.User.JWT_SESSION_KEY: vo.token})
        return BaseResp.ok(data=vo)

    @Post('/login', summary='登录', response_model=BaseResp[LoginVO])
    async def login(self, dto: LoginDTO):
        # 如果该用户被封禁
        user = await User.get_or_none(email=dto.email, status=StatusEnum.NORMAL)
        if user is None:
            raise BusinessException(detail='登录失败，该邮箱未注册或该账号已被封禁，请注册或联系管理员')
        token = await user_service.login(user, dto)
        # session中设置token，以便访问图片
        self.session.update({RequestConstant.User.JWT_SESSION_KEY: token})
        return BaseResp(msg='登录成功', data=LoginVO(token=token))

    @Put('/updatepwd-email', summary='修改密码，需要邮箱验证码')
    async def update_password(self, dto: UpdatePasswordByEmailDTO):
        key = await verify_email_code(self.session, dto.email, dto.code)
        user = await User.get_or_none(email=dto.email)
        if user is None:
            raise BusinessException(detail='该邮箱尚未注册')
        if user.status == StatusEnum.DISABLED:
            raise BusinessException(detail='修改失败，该账号已被删除，请联系管理员')
        await user_service.update_password(user, dto.password)
        redis.delete(key)
        return BaseResp(msg='修改成功')


@Controller(PATH, tags=['用户登录后相关接口'])
class UserNeedLoginController:
    user = use_dep(use_login)

    @Get(summary='用token获取用户详情', response_model=BaseResp[UserVO])
    async def get_uer_info(self):
        return BaseResp.ok(msg='获取成功', data=await user_service.get_user_info(self.user))

    @Put('/updatepwd-pwd', summary='修改密码，需要原密码', response_model=BaseResp[None])
    async def update_password(self, dto: UpdatePasswordByOriDTO):
        await user_service.update_password(self.user, **dto.model_dump())
        return BaseResp(msg='修改成功')

    @Put('/info', summary='修改用户信息', response_model=BaseResp[None])
    async def update_user_info(self, dto: UpdateUserInfoDTO):
        await self.user.update_from_dict({'nickname': dto.nickname}).save()
        return BaseResp.ok(msg='修改成功')
