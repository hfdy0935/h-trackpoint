from tortoise import Model, fields

from enums import StatusEnum
from constants import DB_NAME_DICT


class User(Model):
    id = fields.CharField(max_length=36, pk=True, description="用户id")
    email = fields.CharField(max_length=30, null=True,
                             description="邮箱，可选，可以用github登录")
    nickname = fields.CharField(max_length=20, default='', description="用户昵称")
    password = fields.CharField(max_length=32, description="用户密码md5结果")
    create_time = fields.DatetimeField(description="注册时间")
    update_time = fields.DatetimeField(description="修改时间")
    status = fields.IntEnumField(enum_type=StatusEnum, description="状态，1正常0封禁")
    is_admin = fields.SmallIntField(default=0, description="是否是管理员，0不是1是")
    project_num_limit = fields.SmallIntField(description="用户项目数量限制")
    event_num_limit = fields.SmallIntField(description="用户单个项目的事件数量限制")

    class Meta:
        table = DB_NAME_DICT['user']
