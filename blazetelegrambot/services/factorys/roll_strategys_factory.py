from ...interfaces.signal_strategy import Pattern, SignalStrategy
from ...interfaces.strategy_factory import StrategyFactory
from ...infrastructure.signal_strategys.roll_strategy import RollStrategy
from ...infrastructure.checkers.win_checker import WinChecker
from ...domain.factory.bets import (
    single_black, single_red, single_white, ten_white
)

from typing import Literal

class RollStrategYFactorys(StrategyFactory):
    
    def create(self, signal:Literal[0, 1, 2, 3], pattern: Pattern, broker:str)->SignalStrategy:
        match signal:
            case 3:
                factory = ten_white.TenMinutesWhiteFactory(broker=broker)
        
            case 0:
                factory = single_white.SingleWhiteFactory(broker=broker)
            
            case 1:
                factory = single_red.SingleRedFactory(broker=broker)
            
            case 2:
                factory = single_black.SingleBlackFactory(broker=broker)
            
            case _:
                factory = single_black.SingleBlackFactory(broker=broker)
        
        signal = 0 if signal == 3 else signal
        
        strat = RollStrategy(signal=signal, pattern=pattern, checker=WinChecker(), bet_factory=factory)
        
        return strat