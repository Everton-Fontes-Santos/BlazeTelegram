from pydantic import BaseModel
from collections import deque

from .double import Double


class Roulette(BaseModel):
    doubles:deque[Double] = deque([], maxlen=40)
    
    def __len__(self)->int:
        return len(self.doubles)
    
    def add(self, *doubles:Double):
        for double in doubles:
            self.doubles.append(double)
    
    def last(self)->Double:
        return self.doubles[-1]
    
    def first(self)->Double:
        return self.doubles[0]
    
    def last_n(self, n_doubles:int):
        return list(self.doubles)[-n_doubles:]