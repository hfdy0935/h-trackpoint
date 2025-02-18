from tortoise import Model, fields
from constants import DB_NAME_DICT

from enums import BindParamTypeEnum


class BindParam(Model):
    id = fields.CharField(pk=True, max_length=36, description='id')
    name = fields.CharField(max_length=30, description='参数名')
    description = fields.CharField(
        max_length=300, null=True, description='参数描述')
    type = fields.CharEnumField(
        enum_type=BindParamTypeEnum, description='参数类型列表，暂时只支持number、string、boolean、list、dict，list、dict里面的参数类型不做进一步限制')

    class Meta:
        table = DB_NAME_DICT['bind_param']
        table_description = '绑定参数表，用于约束上传参数，可自定义'
