from blazetelegrambot.interfaces.base_event import DomainEvent
from ..domain.entitys.roulette import Roulette
from ..interfaces.handler import Handler
from ..interfaces.signal_strategy import SignalStrategy
from ..interfaces.message_client import MessageClient
from ..interfaces.service import Service

import json

IDS = list[str|int]

class DoubleSignalSenderHandler(Handler):
    name:str = 'roullete-updated'
    strategys:list[SignalStrategy]
    send_to:dict[str, IDS] = {}
    client:MessageClient
    transform_bet_to_msg:Service
    
    
    def addIds(self, color_name:str, *ids:str|int)->None:
        if not color_name in self.send_to.keys():
            self.send_to[color_name] = list(ids)
            return
        self.send_to[color_name].extend(ids)
    
    async def handle(self, event: DomainEvent) -> None:
        if self.name != event.name:
            return
        
        roulette = Roulette(json.loads(event.data))
        for strategy in self.strategys:
            if strategy.check(roulette):
                output = self.transform_bet_to_msg.execute(strategy.actual_bet.model_dump())
                if output.color in self.send_to.keys():
                    for id in self.send_to[output.color]:
                        await self.client.send_message(output.text, id)