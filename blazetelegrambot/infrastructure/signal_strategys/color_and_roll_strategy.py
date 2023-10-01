from blazetelegrambot.interfaces.signal_strategy import Pattern
from ...interfaces.bet_factory import BetFactory
from ...interfaces.checker import Checker
from ...interfaces.signal_strategy import SignalStrategy, Pattern

from ...domain.entitys.bet import Bet
from ...domain.entitys.double import Double
from ...domain.entitys.roulette import Roulette

class ColorAndRollStrategy(SignalStrategy):
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
    
    def get_pattern_type(self, double:Double)->str:
        tile = 'white'
        if double.color == 2:
            tile = 'black'

        if double.color == 1:
            tile = 'red'
            
        return tile
    
    def equal_patterns(self, patt:Pattern, roulette:Roulette)->bool:
        n_doubles = len(patt)
        roll = roulette.last_n(n_doubles)
        rolled = []
        
        #check the pattern
        for idx, tile in enumerate(patt):
            if isinstance(tile, str):
                match tile.lower():
                    case 'black':             
                        rolled.append(self.get_pattern_type(roll[idx]))
                    case 'red':
                        rolled.append(self.get_pattern_type(roll[idx]))
                    case 'white':
                        rolled.append(self.get_pattern_type(roll[idx]))
                    case 'any':
                        rolled.append('any')
                
            else:
                rolled.append(roll[idx].roll)
        return patt == rolled
    
    def check_pattern(self, roulette:Roulette)->bool:
        if isinstance(self.pattern[0], list):
        
            for patt in self.pattern:
                if self.equal_patterns(patt, roulette):
                    return True
                
            return False
        
        return self.equal_patterns(self.pattern, roulette)
    
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