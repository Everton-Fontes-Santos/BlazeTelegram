from ..interfaces.service import ServiceOutput, ServiceInput, Service
from ..domain.factory.strategy_factory import StrategyFactory

from typing import Literal, Any


class CreateInput(ServiceInput):
    strategy_type:Literal['color', 'white'] = 'color'
    check_type:Literal['color', 'roll', 'any'] = 'color'

class CreateStrategy(Service):
    strategy_factory:StrategyFactory
    
    async def execute(self, input: dict[str, Any]) -> ServiceOutput | None:
        data = CreateInput(**input)
        strategy = StrategyFactory.create(data.strategy_type)      
        
        return strategy