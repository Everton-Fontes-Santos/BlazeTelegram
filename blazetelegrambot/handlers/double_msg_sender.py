from ..interfaces.base_event import DomainEvent
from ..domain.entitys.roulette import Roulette
from ..interfaces.handler import Handler
from ..interfaces.signal_strategy import SignalStrategy
from ..interfaces.message_client import MessageClient
from ..interfaces.service import Service
from .log_handler import logger

import json

IDS = list[str|int]

class DoubleMsgSenderHandler(Handler):
    name:str = 'roullete-updated'
    strategys:list[SignalStrategy]
    send_to:dict[str, IDS] = {}
    send_to_free:dict[str, IDS] = {}
    client:MessageClient
    transform_bet_to_msg_signal:Service
    transform_bet_to_msg_result:Service
    msg_free_counter:int = 5
    
    
    def addIds(self, color_name:str, free:bool=False, *ids:str|int)->None:
        if free:
            print('Adding', ids)
            if not color_name in self.send_to_free.keys():
                self.send_to_free[color_name] = list(ids)
                return
            self.send_to_free[color_name].extend(ids)
            return
        
        print('Adding', ids)
        if not color_name in self.send_to.keys():                 
            self.send_to[color_name] = list(ids)
            return
        
        self.send_to[color_name].extend(ids)
    
    async def handle(self, event: DomainEvent) -> None:
        if self.name != event.name:
            return
        
        roulette = Roulette(**json.loads(event.data))
        
        for strategy in self.strategys:
            
            #send result
            if strategy.actual_bet and strategy.check_win(roulette.last()):
                output = self.transform_bet_to_msg_result.execute(strategy.actual_bet.model_dump())
                if output and output.color in self.send_to.keys():
                    for id in self.send_to[output.color]:
                        await self.client.send_message(output.text, id)
                if output and output.color in self.send_to_free.keys():
                    for id in self.send_to_free[output.color]:
                        await self.client.send_message_by_count(output.text, id, self.msg_free_counter)
                    
            #send signals
            if strategy.check(roulette):
                
                output = self.transform_bet_to_msg_signal.execute(strategy.actual_bet.model_dump())
                if output.color in self.send_to.keys():
                    for id in self.send_to[output.color]:
                        await self.client.send_message(output.text, id)
                        self.client.add()
                if output and output.color in self.send_to_free.keys():
                    for id in self.send_to_free[output.color]:
                        await self.client.send_message_by_count(output.text, id, self.msg_free_counter)