from datetime import datetime
from uuid import uuid4
from fastapi_boot.core import Service

from domain.config import ProjConfig
from domain.dto.user import LoginDTO, RegisterDTO
from domain.entity.event_project import EventProject
from domain.entity.project import Project
from domain.entity.user import User
from domain.entity.custom_event import CustomEvent
from domain.vo.user import RegisterVO, UserVO
from enums import StatusEnum
from exception import BusinessException
from utils import JWTUtil, MD5Util, gid


@Service
class UserService:

    def __init__(self, cfg: ProjConfig, md5: MD5Util, jwt: JWTUtil):
        self.config = cfg.email
        self.project_num_limit = cfg.business.user_project_num_limit
        self.event_num_limit = cfg.business.custom_event_num_limit
        self.md5 = md5
        self.jwt = jwt

    async def register(self, dto: RegisterDTO) -> RegisterVO:
        """注册"""
        userId = gid()
        await User(
            id=userId,
            email=dto.email,
            nickname=dto.nickname,
            password=self.md5.encrypt(dto.password),
            create_time=datetime.now(),
            update_time=datetime.now(),
            status=StatusEnum.NORMAL,
            is_admin=False,
            project_num_limit=self.project_num_limit,
            event_num_limit=self.event_num_limit
        ).save()
        # 生成jwt
        token = self.jwt.create({'id': userId})
        return RegisterVO(token=token)

    async def update_password(self, user: User, new_password: str, ori_password: str | None = None):
        """修改密码，如果ori_password为空表示不需要验证原密码"""
        if (ori_password is not None) and self.md5.encrypt(ori_password) != user.password:
            raise BusinessException(detail='修改失败，旧密码错误')
        rows = await User.filter(id=user.id).update(password=self.md5.encrypt(new_password), update_time=datetime.now())
        if rows == 0:
            raise BusinessException(detail='修改失败')

    async def login(self, user: User, dto: LoginDTO) -> str:
        """登录"""
        if self.md5.encrypt(dto.password) != user.password:
            raise BusinessException(detail='登录失败，密码错误')
        return self.jwt.create({'id': user.id})

    async def get_user_info(self, user: User) -> UserVO:
        """获取用户信息，包括停用的"""
        project_list = await Project.filter(user_id=user.id)
        # 已添加到项目中的事件id列表
        normal_event_id_list = [i.id for i in await EventProject.filter(project_id__in=[i.id for i in project_list])]
        # 没添加到任何项目的事件id列表，只有自定义事件
        other_event_id_list = [i.id for i in await CustomEvent.filter(user_id__in=[user.id])]
        return UserVO(
            id=user.id,
            email=user.email,
            nickname=user.nickname,
            createTime=user.create_time,
            projectNumLimit=user.project_num_limit,
            eventNumLimit=user.event_num_limit,
            projectNum=len(project_list),
            eventNum=len(set([*normal_event_id_list, *other_event_id_list]))
        )
