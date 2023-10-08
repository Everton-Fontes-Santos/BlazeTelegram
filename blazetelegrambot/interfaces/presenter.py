from abc import ABC, abstractmethod
from pydantic import BaseModel


class Presenter(ABC, BaseModel):
    
    @abstractmethod
    def stop(self)->None:
        ...
    
    @abstractmethod
    def listen(self, in_thread:bool=True)->None:
        ...