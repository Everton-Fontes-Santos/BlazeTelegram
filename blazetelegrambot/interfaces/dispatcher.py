from abc import ABC, abstractmethod
from pydantic import BaseModel

from .base_event import DomainEvent
from .handler import Handler


class Dispatcher(ABC, BaseModel):
    
    @abstractmethod
    def register(self, handler:Handler)->None:
        ...
    
    @abstractmethod
    def publish(self, event:DomainEvent)->None:
        ...
    