from abc import ABC, abstractmethod
from pydantic import BaseModel

class MessageClient(ABC, BaseModel):
    counter:int
    
    @abstractmethod
    def send_message(self, msg:str, id_to_send:str|int)->None:
        ...
        
    @abstractmethod
    def send_message_by_count(self, msg:str, id_to_send:str|int, count:int)->None:
        ...