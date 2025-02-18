from tortoise import fields, Model
from tortoise.indexes import Index
from constants import DB_NAME_DICT

class EventProject(Model):
    id = fields.CharField(pk=True, max_length=36, description='id')
    event_id = fields.CharField(max_length=36, description='用户事件id')
    project_id = fields.CharField(max_length=36, description='项目id')

    class Meta:
        table = DB_NAME_DICT['event_project']
        table_description = '用户事件和项目关联表'
        indexes = [
            Index(fields=('event_id',), name='idx_custom_event_id'),
            Index(fields=('project_id',), name='idx_project_id'),
        ]
