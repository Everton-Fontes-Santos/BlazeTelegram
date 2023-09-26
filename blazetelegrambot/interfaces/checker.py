from abc import ABC, abstractmethod
from pydantic import BaseModel
from datetime import datetime

from ..domain.entitys.bet import Bet
from ..domain.entitys.double import Double


class Checker(ABC, BaseModel):
    counter:int
    
    @abstractmethod
    def can_check(self, bet:Bet, time:datetime)->bool:
        ...
    
    @abstractmethod
    def check(self, bet:Bet, double:Double):
        ...