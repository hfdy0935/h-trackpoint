from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    host: str = 'localhost'
    port: int = 8000
    reload: bool = True


class MySqlConfig(BaseModel):
    host: str = 'localhost'
    port: int = 3306
    username: str
    password: str | int
    db: str


class TortoiseConfig(BaseModel):
    models: list[str]


class RedisConfig(BaseModel):
    host: str = 'localhost'
    port: int = 6379
    db: int = 0


class MinIOConfig(BaseModel):
    endpoint: str
    bucket: str
    user: str = Field(description="access_key")
    password: str = Field(description="secret_key")
    secure: bool = Field(description="使用http还是https")


class EmailConfig(BaseModel):
    host: str
    username: str
    password: str


class JwtConfig(BaseModel):
    access_tokne_expires: int = 20*60  # 20min
    refresh_token_expires: int = 3600*2  # 2h
    algorithm: str = 'HS256'
    secret_key: str = 'trackpoint-peoject'
    token_key: str = 'Authorization'


class BusinessConfig(BaseModel):
    user_project_num_limit: int
    custom_event_num_limit: int


class ProjConfig(BaseModel):
    server: ServerConfig
    mysql: MySqlConfig
    tortoise: TortoiseConfig
    redis: RedisConfig
    minio: MinIOConfig
    email: EmailConfig
    jwt: JwtConfig
    business: BusinessConfig
