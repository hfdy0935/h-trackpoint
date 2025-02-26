from fastapi import FastAPI, Request
from fastapi_boot.core import Lifespan, Inject, ExceptionHandler, Bean
from minio import Minio


from constants import CacheConstant
from domain.config import ProjConfig
from domain.entity.default_event import DefaultEvent
from domain.vo.common import BaseResp
from exception import BusinessException
from helper import HBF


async def init_mysql():
    from tortoise import Tortoise
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


def init_minio_image():
    """把测试点击图片添加到minio"""
    cfg = Inject(ProjConfig).minio
    minio = Inject(Minio)
    if not minio.bucket_exists(cfg.bucket):
        minio.make_bucket(cfg.bucket)
    minio.fput_object(
        bucket_name=cfg.bucket,
        object_name='22973563910f1eda3d79254d67c215aa.png',
        file_path='resources/22973563910f1eda3d79254d67c215aa.png',
        content_type='image/png',
    )


@Lifespan
async def lifespan(app: FastAPI):
    from tortoise import BaseDBAsyncClient, Tortoise
    await init_mysql()
    conn: BaseDBAsyncClient = Tortoise.get_connection('default')
    await add_default_event_id_list_to_bloom_filter()
    init_minio_image()

    @Bean
    def _() -> BaseDBAsyncClient:
        return conn
    yield
    await conn.close()


@ExceptionHandler(BusinessException)
def _(r: Request, exp: BusinessException):
    return BaseResp(code=exp.status_code, msg=exp.detail)
