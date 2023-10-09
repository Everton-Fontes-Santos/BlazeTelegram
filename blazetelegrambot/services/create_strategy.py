from ..interfaces.service import ServiceOutput, ServiceInput, Service
from ..interfaces.strategy_factory import StrategyFactory, SignalStrategy, Pattern

from typing import Literal, TypedDict

SignalType = Literal[0, 1, 2, 3]
class InputDict(TypedDict):
    signal:SignalType
    broker:str
    pattern:Pattern

class CreateInput(ServiceInput):
    signal:SignalType = 1
    broker:str = 'blaze'
    pattern:Pattern


class CreateOutput(ServiceOutput):
    strategy:SignalStrategy

class CreateStrategy(Service):
    strategy_factory:StrategyFactory
    
    async def execute(self, input: InputDict) -> CreateOutput| None:
        data = CreateInput(**input)
        strategy = self.strategy_factory.create(data.signal, data.pattern, data.broker)      
        
        return CreateOutput(strategy=strategy)