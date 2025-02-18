class CacheConstant:
    """redis常量"""
    EMAIL_CODE = 'email_code'  # 邮件验证码缓存的key
    EXPIRES = 5 * 60  # 过期时间5分钟
    SCREENSHOT_BF_NAME = 'screen_bf_name'  # 截图布隆过滤器key
    DEFAULT_EVENT_BF_NAME = 'default_event_bf_name'  # 默认事件id布隆过滤器的key


class EmailConstant:
    """邮件常量"""
    TEMPLATE_CODE_PLACEHOLDER = '{{code}}'  # 验证码占位符
    TEMPLATE_MINUTE_PLACEHOLDER = '{{minute}}'  # 有效时间占位符，单位是分钟


# 静态资源（图片）url路径的前缀
RESOURCE_PREFIX = 'resource'

# yyyy-MM-dd hh:mm:ss格式的时间正则表达式
FORMAT_DATETIME_PATTERN = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'


class RequestConstant:
    """请求头字段key常量"""
    class User:
        SESSION_ID = 'session_id'  # 用户注册时
        JWT_HEADER_KEY = 'Authorization'  # jwt在请求头中的key
        JWT_SESSION_KEY = 'jwt_session_key'  # jwt在session中的key，用于控制台请求图片时验证身份

    class Client:
        PROJECT_ID = 'project_id'  # 客户端项目id


DB_NAME_DICT = {
    'default_event': 'default_event',
    'custom_event': 'custom_event',
    'bind_param': 'bind_param',
    'event_project': 'event_project',
    'event_bind_param': 'event_bind_param',
    'project': 'project',
    'user': 'user',
    'record': 'record',
    'client': 'client'
}
"""数据库名字典"""
