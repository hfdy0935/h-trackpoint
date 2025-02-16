from domain.dto.client import ClientSendEventsDTO
from domain.entity.default_event import DefaultEvent
from domain.entity.custom_event import CustomEvent

ClientSendEventsBO = tuple[ClientSendEventsDTO,
                           list[DefaultEvent | CustomEvent], str, str]
"""上报事件时Controller给Service的参数"""
