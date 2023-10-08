from abc import ABC, abstractmethod
from pydantic import BaseModel

class HTTPClient(ABC, BaseModel):
    
    @abstractmethod
    async def get(self, url:str)->dict:
        ...
    
    @abstractmethod
    async def post(self, url:str, data:dict)->dict:
        ...
        