import os
from fastapi_boot.core import Bean, Inject
from minio import Minio
import yaml
from redis import Redis
from domain.config import BusinessConfig, MinIOConfig, ProjConfig, RedisConfig, ServerConfig, MySqlConfig, TortoiseConfig, JwtConfig, EmailConfig

CONFIG_YML_PATH = './resource/config.docker.yml' if os.environ.get(
    'DOCEKR') else './resource/config.yml'


@Bean
def _cfg() -> ProjConfig:
    with open(CONFIG_YML_PATH, 'r') as f:
        data = yaml.safe_load(f)
        return ProjConfig(
            server=ServerConfig(**data['server']),
            mysql=MySqlConfig(**data['mysql']),
            tortoise=TortoiseConfig(**data['tortoise']),
            redis=RedisConfig(**data['redis']),
            minio=MinIOConfig(**data['minio']),
            email=EmailConfig(**data['email']),
            jwt=JwtConfig(**data.get('jwt', {})),
            business=BusinessConfig(**data['business'])
        )


@Bean
def init_redis() -> Redis:
    c = Inject(ProjConfig).redis
    return Redis(c.host, c.port, c.db, decode_responses=True)


@Bean
def init_minio() -> Minio:
    c = Inject(ProjConfig).minio
    instance = Minio(c.endpoint, c.user, c.password, secure=c.secure)
    if not instance.bucket_exists(c.bucket):
        instance.make_bucket(c.bucket)
    return instance
