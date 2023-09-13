from pydantic import BaseModel

from ...interfaces.base_event import DomainEvent
from ...interfaces.dispatcher import Dispatcher


from datetime import datetime

class EventFactory(BaseModel):
    """The Event Factory its a factory thats broke the SRP,
    but will be very usefull in the aplication,
    he will be able to just create a event, and create a event and send to handlers

    Returns:
        DomainEvent: The Event of type choosed
    """
    mediator:Dispatcher| None = None

    @staticmethod
    def create(name:str, data:str, occured:datetime|str=None)->DomainEvent:
        time = datetime.now()
        if occured and isinstance(occured, str):
            time = datetime.strptime(occured, "%Y-%m-%d %H:%M:%S")
            
        if occured and isinstance(occured, datetime):
            time = occured
            
        return  DomainEvent(
            name=name,
            data=data,
            ocurred=time
        )
        

    async def create_and_publish(self, name:str, data:str, occured:datetime|str=None)->DomainEvent:
        time = datetime.now()
        if occured and isinstance(occured, str):
            time = datetime.strptime(occured, "%Y-%m-%d %H:%M:%S")
            
        if occured and isinstance(occured, datetime):
            time = occured
            
        event =  DomainEvent(
            name=name,
            data=data,
            ocurred=time
        )
        if self.mediator:
            await self.mediator.publish(event)
        
        return event