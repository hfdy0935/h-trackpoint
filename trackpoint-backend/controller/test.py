import asyncio
import random
from fastapi import HTTPException
from fastapi_boot.core import Controller,  Post

from domain.vo.common import BaseResp
from exception import BusinessException


@Controller('/v1/test',tags=['调试'])
class TestController:
    """后台测试页面"""

    @Post('/random-result', summary='测试请求上报事件，结果随机', response_model=BaseResp[None])
    async def test_request_send_event(self):
        i = random.randint(1, 3)
        await asyncio.sleep(i)
        if i == 1:
            raise HTTPException(status_code=500, detail='请求失败')
        elif i == 2:
            return BaseResp.ok()
        else:
            raise BusinessException(detail='请求失败')
