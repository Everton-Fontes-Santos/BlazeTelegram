from pydantic import BaseModel
from datetime import datetime



class Bet(BaseModel):
    init_time:datetime
    start_time:datetime
    mid_time:datetime = None
    end_time:datetime
    signal:int
    active:bool = True
    broker:str
    win:str = ''
    
    def is_active(self, time:datetime)->bool:
        self.active = False
        
        if time.time() >= self.init_time.time() and time.time() <= self.end_time.time():
            self.active = True
        if time.minute == self.end_time.minute and time.second >=30:
            self.active = True
            
        return self.active