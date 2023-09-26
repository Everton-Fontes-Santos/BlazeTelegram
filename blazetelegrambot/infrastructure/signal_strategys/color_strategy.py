
from ...interfaces.signal_strategy import SignalStrategy
from ...interfaces.checker import Checker

from ...domain.entitys.bet import Bet
from ...domain.entitys.roulette import Roulette
from ...domain.entitys.double import Double

from ...interfaces.bet_factory import BetFactory


class ColorStrategy(SignalStrategy):
    signal:int = 0
    pattern:list[int|list[int]] = []
    bet_factory:BetFactory = None
    actual_bet:Bet = None
    changed:bool = False
    checker:Checker
    
    def check_win(self, double:Double):
        return self.checker.check(self.actual_bet, double)
    
    def check_pattern(self, roulette:Roulette)->bool:
        match self.read_type:
            case 'color':
                if isinstance(self.pattern[0], list):
                    
                    for patt in self.pattern:
                        n_doubles = len(patt)
                        roll = [ double.color for double in roulette.last_n(n_doubles)]
                        print(roll)
                        print(patt)
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
                return

                
            if self.actual_bet and not self.check_active_bet(roulette):
                bet = self.create_bet(roulette)
                if bet != self.actual_bet:
                    self.actual_bet = bet
                    self.changed = True
                    return
            
            self.changed = False
        self.changed = False
                
                
# case 'roll':
                
#     if isinstance(self.pattern[0], list):
        
#         for patt in self.pattern:
#             n_doubles = len(patt)
#             roll = [ double.roll for double in roulette.last_n(n_doubles)]
#             print(roll)
#             print(patt)
#             if patt ==  roll:
#                 return True
#         return False
#     else:
#         n_doubles = len(self.pattern)
#         roll = [ double.roll for double in roulette.last_n(n_doubles)] 
#         return self.pattern ==  roll