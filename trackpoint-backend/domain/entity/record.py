from tortoise import Model, fields
from tortoise.indexes import Index
from constants import DB_NAME_DICT

class Record(Model):
    id = fields.CharField(max_length=36, pk=True, description='记录id')
    project_id = fields.CharField(
        max_length=36, null=False, description='项目id')
    event_id = fields.CharField(max_length=36, null=False, description='事件id')
    client_id = fields.CharField(
        max_length=36, null=False, description='客户端id')
    create_time = fields.DatetimeField(null=False, description='创建时间')
    page_url = fields.CharField(
        max_length=100, null=False, description='页面url')
    screen_shot_path = fields.CharField(
        max_length=100, null=True, description='截图路径，如有')
    params = fields.JSONField(null=True, description='参数')

    class Meta:
        table = DB_NAME_DICT['record']
        table_description = "上报记录表"
        indexes = [
            Index(fields=("event_id",), name="idx_event_id"),
            Index(fields=("device_id",), name="idx_device_id")
        ]
