from tortoise import Model, fields
from enums import StatusEnum


class DefaultEvent(Model):
    id = fields.CharField(max_length=36, pk=True, description='事件id')
    name = fields.CharField(max_length=30, null=False, description='事件名')
    description = fields.TextField(null=True, description='事件描述')
    need_shot = fields.BooleanField(
        null=False, default=0, description='事件触发时是否需要截图')
    status = fields.IntEnumField(enum_type=StatusEnum, description="状态，1正常0下架")

    class Meta:
        table = "default_event"
        table_description = "默认事件表"
