from tortoise import fields, Model
from tortoise.indexes import Index
from constants import DB_NAME_DICT

class EventBindParam(Model):
    id = fields.CharField(pk=True, max_length=36, description='id')
    event_id = fields.CharField(max_length=36, description='事件id')
    bind_param_id = fields.CharField(max_length=36, description='绑定参数id')

    class Meta:
        table = DB_NAME_DICT['event_bind_param']
        table_description = '事件绑定参数关联表'
        indexes = [
            Index(fields=('event_id',), name='idx_event_id'),
            Index(fields=('bind_param_id',), name='idx_bind_param_id'),
        ]