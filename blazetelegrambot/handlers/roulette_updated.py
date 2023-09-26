from ..domain.factory.event_factory import EventFactory
from ..domain.entitys import roulette

from ..interfaces.signal_strategy import SignalStrategy
from ..interfaces.handler import Handler
from ..interfaces.base_event import DomainEvent

from pydantic import BaseModel
from datetime import datetime
import json

class BetResult(BaseModel):
    time:datetime
    result:str
    signal:int

class RouletteUpdatedHandler(Handler):
    name:str = "roulette-updated"
    strategys: list[SignalStrategy]
    event_factory:EventFactory
    last:roulette.Roulette = None
        
    async def handle(self, event:DomainEvent)->None:
        if event.name != self.name:
            return
        
        try:
            roll = roulette.Roulette(json.loads(event.data))
        except:
            return
        
        if self.last:
        
            if str(self.last.last().creation_time) == str(roll.last().creation_time):
                return
        
        self.last = roll
        
        for strategy in self.strategys:
            await self.check_bet_result_and_publish(strategy, roll)
            await self.check_roulette(strategy, roll)
            await self.check_bet_and_publish(strategy)
    
    async def check_roulette(self, strategy:SignalStrategy, roll: roulette.Roulette):
        strategy.check(roll)
    
    async def check_bet_and_publish(self, strategy:SignalStrategy):
        if strategy.new_bet() and strategy.actual_bet:
            await self.event_factory.create_and_publish("double-signal", strategy.actual_bet.model_dump_json())
            
    async def check_bet_result_and_publish(self, strategy:SignalStrategy, roll:roulette.Roulette):
            
        if strategy.actual_bet and strategy.check_win(roll.last()):
            result = BetResult(
                time=roll.last().creation_time,
                result=strategy.actual_bet.win,
                signal=strategy.actual_bet.signal
            )  
        
            await self.event_factory.create_and_publish("double-result", result.model_dump_json())