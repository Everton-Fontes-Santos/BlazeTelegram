from abc import ABC, abstractmethod
from pydantic import BaseModel

from ..domain.entitys.bet import Bet
from ..domain.entitys.double import Double
from ..domain.entitys.roulette import Roulette


class SignalStrategy(ABC, BaseModel):
        
    @abstractmethod
    def check_win(self, double:Double)->bool:
        ...
    
    @abstractmethod
    def check_pattern(self, roulette:Roulette)->bool:
        ...
    
    @abstractmethod
    def create_bet(self, roulette:Roulette)->Bet:
        ...
    
    @abstractmethod
    def check(self, roulette:Roulette)->None:
        ...