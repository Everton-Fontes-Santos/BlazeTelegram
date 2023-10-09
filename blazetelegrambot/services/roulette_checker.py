from typing import Any
from ..interfaces.service import Service, ServiceOutput
from ..domain.entitys.roulette import Roulette
from ..domain.entitys.server_double import ServerDouble, DoubleRecents
from ..domain.entitys.double import Double
from ..domain.factory.double_factory import DoubleFactory
from ..interfaces.http import HTTPClient


from datetime import timedelta

class OutPut(ServiceOutput):
    roulette:Roulette

class RouletteChecker(Service):
    web_client:HTTPClient
    url_latest:str = "https://blaze.com/api/roulette_games/recent"
    
    async def execute(self, _: dict[str, Any])->OutPut:
        data = await self.web_client.get(self.url_latest)
        roulette = Roulette()
        if not data:
            return 
        
        doubles = handle_data(data)
        roulette.add(*doubles[::-1])

        return OutPut(roulette=roulette)
    
    
    
def handle_data(data:dict, diference_time:int=3, broker:str='blaze')->list[Double]:
    try:
        last_doubles= DoubleRecents(doubles=[ServerDouble(**d) for d in data])
    except Exception as e:
        print(e)
        return
    
    doubles = []
    for double in last_doubles.doubles:
        doubles.append(
            DoubleFactory.create(
                broker,
                double.roll,
                double.created_at - timedelta(hours=diference_time),
                double.id
            )
        )
    return doubles