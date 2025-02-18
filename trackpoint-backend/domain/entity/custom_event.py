from tortoise import Model, fields
from tortoise.indexes import Index

from enums import StatusEnum
from constants import DB_NAME_DICT


class CustomEvent(Model):
    id = fields.CharField(max_length=36, pk=True, description='事件id')
    name = fields.CharField(max_length=30, null=False, description='事件名')
    description = fields.TextField(null=True, description='事件描述')
    user_id = fields.CharField(max_length=36, null=False, description='所属用户id')
    create_time = fields.DatetimeField(null=False, description='创建时间')
    update_time = fields.DatetimeField(null=False, description='修改时间')
    status = fields.IntEnumField(enum_type=StatusEnum, description="状态，1正常0下架")

    class Meta:
        table = DB_NAME_DICT['custom_event']
        table_description = "自定义事件"
        indexes = [
            Index(fields=('name',), name="idx_name"),
            Index(fields=('user_id',), name="idx_user_id"),
        ]
