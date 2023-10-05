
from ...interfaces.signal_strategy import SignalStrategy, Pattern
from ...interfaces.checker import Checker

from ...domain.entitys.bet import Bet
from ...domain.entitys.roulette import Roulette
from ...domain.entitys.double import Double

from ...interfaces.bet_factory import BetFactory


class ColorStrategy(SignalStrategy):
    signal:int = 0
    pattern:list[Pattern] | Pattern = []
    bet_factory:BetFactory = None
    actual_bet:Bet = None
    changed:bool = False
    checker:Checker
    
    def set_pattern(self, pattern: Pattern | list[Pattern]):
        self.pattern = pattern
    
    def check_win(self, double:Double):
        return self.checker.check(self.actual_bet, double)
    
    def check_pattern(self, roulette:Roulette)->bool:
        if isinstance(self.pattern[0], list):
            
            for patt in self.pattern:
                n_doubles = len(patt)
                roll = [ double.color for double in roulette.last_n(n_doubles)]
                
                if patt ==  roll:
                    return True
            return False
        else:
            n_doubles = len(self.pattern)
            roll = [ double.color for double in roulette.last_n(n_doubles)] 
            return self.pattern ==  roll
    
    def create_bet(self, roulette:Roulette)->Bet:
        if self.bet_factory:
            return self.bet_factory.create(roulette)
    
    def check_active_bet(self, roulette:Roulette):
        
        return self.actual_bet.is_active(roulette.last().creation_time)
    
    def new_bet(self)->bool:
        return self.changed
            
    def check(self, roulette:Roulette):
        if self.check_pattern(roulette):
            
            if not self.actual_bet:
                self.actual_bet = self.create_bet(roulette)
                self.changed = True
                return True

                
            if self.actual_bet and not self.check_active_bet(roulette):
                bet = self.create_bet(roulette)
                if bet != self.actual_bet:
                    self.actual_bet = bet
                    self.changed = True
                    return True
            
            self.changed = False
        self.changed = False
        return False