from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Literal

from ..domain.entitys.bet import Bet
from ..domain.entitys.double import Double
from ..domain.entitys.roulette import Roulette

Rolls = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
Colors = Literal['black', 'red', 'white']
Any_type = Literal['any']
SignalType = Literal[0,1,2]

Pattern = list[Rolls | Colors | Any_type]

class SignalStrategy(ABC, BaseModel):
    actual_bet:Bet
    pattern:Pattern
    signal:SignalType
    
    @abstractmethod
    def set_pattern(self, pattern:Pattern | list[Pattern])->None:
        ...
        
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