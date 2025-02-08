from fastapi import HTTPException


class BusinessException(HTTPException):
    def __init__(self, status_code: int = 500, detail: str = '请求失败'):
        super().__init__(status_code, detail)
