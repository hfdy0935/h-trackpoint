from tortoise import Model, fields
from tortoise.indexes import Index

from enums import StatusEnum
from constants import DB_NAME_DICT

class Project(Model):
    id = fields.CharField(max_length=36, pk=True, description="项目id")
    name = fields.CharField(max_length=20, description="项目名")
    description = fields.CharField(max_length=300, description='项目描述')
    user_id = fields.CharField(max_length=36, description="所属用户id")
    key = fields.CharField(max_length=36, description="项目的key，md5加密，只允许看一次")
    create_time = fields.DatetimeField(description="创建时间")
    update_time = fields.DatetimeField(description="修改时间")
    status = fields.IntEnumField(enum_type=StatusEnum, description="状态，1正常0下架")

    class Meta:
        table = DB_NAME_DICT['project']
        description = "项目表"
        indexes = Index(fields=('user_id',), name="idx_user_id"),
