from queue import Queue
from fastapi_boot.core import Bean
from domain.bo.client import ClientSendEventsBO


@Bean
def _() -> Queue[ClientSendEventsBO]:
    """储存上报事件时Controller给Service的参数的队列"""
    return Queue[ClientSendEventsBO]()
