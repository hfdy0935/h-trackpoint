import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_boot.core import provide_app, Inject

app = provide_app(FastAPI())
app.add_middleware(SessionMiddleware, secret_key='session')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
if __name__ == '__main__':
    from domain.config import ProjConfig
    config = Inject(ProjConfig).server
    uvicorn.run('main:app', host=config.host,
                port=config.port, reload=config.reload)

# 删除所有__pychache__文件夹
# Get-ChildItem -Path . -Recurse -Directory -Filter __pycache__ | Remove-Item -Force -Recurse
