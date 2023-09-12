from abc import ABC, abstractmethod
from pydantic import BaseModel

from .base_event import DomainEvent

class Handler(ABC, BaseModel):
    
    @abstractmethod
    async def handle(self, event:DomainEvent)->None:
        ...
