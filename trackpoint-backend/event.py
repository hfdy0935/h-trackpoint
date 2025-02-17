import asyncio
from fastapi import FastAPI, Request
from fastapi_boot.core import Lifespan, Inject, ExceptionHandler, Bean


from constants import CacheConstant
from domain.config import ProjConfig
from domain.entity.default_event import DefaultEvent
from domain.vo.common import BaseResp
from exception import BusinessException
from helper import HBF


async def init_mysql():
    from tortoise import BaseDBAsyncClient, Tortoise
    config = Inject(ProjConfig)
    mysql = config.mysql
    url = f"mysql://{mysql.username}:{mysql.password}@{mysql.host}:{mysql.port}/{mysql.db}"
    models = config.tortoise.models
    await Tortoise.init(db_url=url, modules=dict(models=models), timezone='Asia/Shanghai')
    # await Tortoise.generate_schemas()


async def add_default_event_id_list_to_bloom_filter():
    """把默认事件id添加到布隆过滤器"""
    bf = Inject(HBF, CacheConstant.DEFAULT_EVENT_BF_NAME)
    defaule_event_id_list = [i.id for i in await DefaultEvent.all()]
    bf.add(CacheConstant.DEFAULT_EVENT_BF_NAME, *defaule_event_id_list)


@Lifespan
async def lifespan(app: FastAPI):
    from tortoise import BaseDBAsyncClient, Tortoise
    # 睡会，等mysql启动完毕
    # await asyncio.sleep(10)
    await init_mysql()
    conn: BaseDBAsyncClient = Tortoise.get_connection('default')
    await add_default_event_id_list_to_bloom_filter()

    @Bean
    def _() -> BaseDBAsyncClient:
        return conn
    yield
    await conn.close()


@ExceptionHandler(BusinessException)
def _(r: Request, exp: BusinessException):
    return BaseResp(code=exp.status_code, msg=exp.detail)
