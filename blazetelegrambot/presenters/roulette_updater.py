from ..interfaces.presenter import Presenter
from ..interfaces.service import Service
from ..domain.entitys.double import Double
from ..domain.factory.event_factory import EventFactory

import time

class RouletteUpdater(Presenter):
    roulette_checker:Service
    add_double:Service
    last_double:Double = None
    running:bool = True
    
    def stop(self):
        self.running = False
    
    async def listen(self) -> None:
        while self.running:
            try:
                actual_roulette = await self.roulette_checker.execute({})
            except:
                pass
            
            if self.last_double and actual_roulette.last() != self.last_double:
                self.last_double = actual_roulette.last()
                await self.add_double.execute({'doubles':[
                    self.last_double.model_dump()
                ]})
            
            if not self.last_double:
                self.last_double = actual_roulette.last()
                await self.add_double.execute({'doubles':[
                    self.last_double.model_dump()
                ]})
                
            time.sleep(5)