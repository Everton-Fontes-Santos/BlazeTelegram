from rich import print
from datetime import datetime

from ...interfaces.checker import Checker, Bet, Double

class WinChecker(Checker):
    counter:int = 0    

    def can_check(self, bet:Bet, time:datetime)->bool:
        return time.time() >= bet.start_time.time()
    
    def check(self, bet:Bet, double:Double):
            
        if not self.can_check(bet, double.creation_time):
            return
        
        if not "GALE" in bet.win and bet.win != "":
            return
        
        if double.color == bet.signal:
            
            bet.win = "WIN"
            self.counter = 0
            
        else:
            self.counter += 1
            bet.win = f"GALE {self.counter}"
            
            if double.creation_time.time() >= bet.end_time.time():
                bet.win = "LOSS"
                self.counter = 0
        
        print(f'Cheking bet: {bet.signal} -> {bet.end_time} with roll {double.color} -> {double.creation_time}')
        print(f"Result -> {bet.win}")
        
        return bet
        
    
    
    