from enum import IntEnum, StrEnum


class StatusEnum(IntEnum):
    """项目、事件、用户的状态"""
    NORMAL = 1  # 正常
    DISABLED = 0  # 下架/封禁
    


class EventTypeEnum(StrEnum):
    """事件类型枚举"""
    DEFAULT = "default"
    """默认事件"""
    CUSTOM = "custom"
    """自定义事件"""


class BindParamTypeEnum(StrEnum):
    """事件绑定参数类型枚举"""
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


class ClientDeviceEnum(StrEnum):
    """客户端设备类型枚举"""
    MOBILE = "mobile"
    TABLET = "tablet"
    CONSOLE = "console"
    SMARTTV = "smarttv"
    WEARABLE = "wearable"
    XR = "xr"
    EMBEDDED = "embedded"
