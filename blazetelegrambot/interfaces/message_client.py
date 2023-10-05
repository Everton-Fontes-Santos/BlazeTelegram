from abc import ABC, abstractmethod
from pydantic import BaseModel

class MessageClient(ABC, BaseModel):
    
    @abstractmethod
    def send_message(self, msg:str, id_to_send:str|int)->None:
        ...