from abc import ABC, abstractmethod
from pydantic import BaseModel

from ..domain.entitys.bet import Bet
from ..domain.entitys.roulette import Roulette


class BetFactory(ABC, BaseModel):
    broker:str
    
    @abstractmethod
    def create(self, roulette:Roulette)->Bet:
        ...