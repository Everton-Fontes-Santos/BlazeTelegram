from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Coroutine, Optional


class APIHandler(ABC, BaseModel):
    path:str
    method:str
    response_model: Optional[BaseModel]
    
    @abstractmethod
    def get_callback(self)->Coroutine:
        ...