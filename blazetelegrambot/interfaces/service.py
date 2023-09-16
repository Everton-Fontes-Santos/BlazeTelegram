from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any


class ServiceInput(BaseModel):
    ...


class ServiceOutput(BaseModel):
    ...


class Service(ABC, BaseModel):
    
    @abstractmethod
    async def execute(self, input:dict[str, Any])->ServiceOutput | None:
        ...