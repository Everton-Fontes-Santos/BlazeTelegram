from ..domain.factory.event_factory import EventFactory
from ..domain.entitys import roulette, double

from ..interfaces.service import Service


class AddDouble(Service):
    roulette:roulette.Roulette
    event_factory:EventFactory
    
    async def execute(self, input:list[dict]):
        try:
            data = [double.Double(**input_) for input_ in input]
        except:
            return
        
        self.roulette.add(*data)
        
        
        await self.event_factory.create_and_publish("roulette-updated", self.roulette.model_dump_json())