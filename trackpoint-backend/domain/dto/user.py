from pydantic import BaseModel, EmailStr, Field


class SendEmailCodeDTO(BaseModel):
    """发送那个邮件验证码请求体"""
    email: EmailStr


class RegisterDTO(SendEmailCodeDTO):
    """注册请求体"""
    email: EmailStr
    password: str = Field(pattern=r'^[0-9a-zA-Z$#@_]{6,12}$')
    nickname: str = ''
    code: str = Field(min_length=6, max_length=6)


class UpdatePasswordByEmailDTO(BaseModel):
    """通过邮件验证码修改密码请求体"""
    email: EmailStr
    password: str = Field(pattern=r'^[0-9a-zA-Z$#@_]{6,12}$')
    code: str = Field(min_length=6, max_length=6)


class UpdatePasswordByOriDTO(BaseModel):
    """通过原密码修改密码请求体"""
    ori_password: str = Field(
        pattern=r'^[0-9a-zA-Z$#@_]{6,12}$', alias='oriPassword')
    new_password: str = Field(
        pattern=r'^[0-9a-zA-Z$#@_]{6,12}$', alias='newPassword')


class LoginDTO(BaseModel):
    """登录请求体"""
    email: EmailStr
    password: str = Field(
        pattern=r'^[0-9a-zA-Z$#@_]{6,12}$', description='密码必须由6-12位的数字、英文大小写字母、@、#、_和$组成')


class UpdateUserInfoDTO(BaseModel):
    """修改用户信息请求体，目前只考虑昵称"""
    nickname: str
