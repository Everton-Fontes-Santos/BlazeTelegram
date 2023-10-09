from ..domain.factory.event_factory import EventFactory
from ..domain.entitys import roulette, double

from ..interfaces.service import Service, ServiceInput

from rich import print

class Input(ServiceInput):
    doubles:list[double.Double]

class AddDouble(Service):
    roulette:roulette.Roulette
    event_factory:EventFactory
    
    async def execute(self, input:dict):
        _input = Input(**input)
        
        self.roulette.add(*_input.doubles)
        
        
        await self.event_factory.create_and_publish("roulette-updated", self.roulette.model_dump_json())