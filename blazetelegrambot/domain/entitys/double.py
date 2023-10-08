from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime, timedelta

class Double(BaseModel):
    color:int
    roll:int
    creation_time:datetime
    broker:str
    
    def __eq__(self, __value: Double) -> bool:
        return self.creation_time.time() == __value.creation_time.time()
    
    def next_time(self)->datetime:
        return self.creation_time + timedelta(seconds=30)
    
    def is_red(self)->bool:
        return self.color == 1
    
    def is_black(self)->bool:
        return self.color == 2
    
    def is_white(self)->bool:
        return self.color == 0

    def next_x_time(self, doubles:int)->datetime:
        return self.creation_time + timedelta(seconds=(30*doubles))
    
    def same_day(self, double:Double)->bool:
        return double.creation_time.day == self.creation_time.day