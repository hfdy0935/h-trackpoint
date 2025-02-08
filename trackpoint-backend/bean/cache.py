from fastapi_boot.core import Bean
from redis import Redis

from constants import CacheConstant
from helper import HBF


@Bean(CacheConstant.SCREENSHOT_BF_NAME)
def _(redis: Redis):
    """截图布隆过滤器"""
    return HBF(redis, CacheConstant.SCREENSHOT_BF_NAME)


@Bean(CacheConstant.DEFAULT_EVENT_BF_NAME)
def _(redis: Redis):
    """默认事件id布隆过滤器"""
    return HBF(redis, CacheConstant.DEFAULT_EVENT_BF_NAME)
