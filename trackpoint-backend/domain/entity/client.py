from tortoise import Model, fields

from enums import ClientDeviceEnum


class Client(Model):
    id = fields.CharField(max_length=36, pk=True,
                          description='设备uid，由前端生成，注册时为每个客户端生成一个')
    os = fields.CharField(max_length=20, null=True, description='操作系统')
    os_version = fields.CharField(
        max_length=20, null=True, description='操作系统版本')
    browser = fields.CharField(max_length=20, null=True, description='浏览器')
    browser_version = fields.CharField(
        max_length=20, null=True, description='浏览器版本')
    device = fields.CharEnumField(
        enum_type=ClientDeviceEnum, null=True, description='设备类型')
    lng = fields.FloatField(default=361, description='经度')
    lat = fields.FloatField(default=361, description='纬度')

    class Meta:
        table = "client"
        table_description = "客户端表"
