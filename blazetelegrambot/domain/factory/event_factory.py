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
    def create(name:str, data:str, ocurred:datetime|str=None)->DomainEvent:
        time = datetime.now()
        if ocurred and isinstance(ocurred, str):
            time = datetime.strptime(ocurred, "%Y-%m-%d %H:%M:%S")
            
        if ocurred and isinstance(ocurred, datetime):
            time = ocurred
            
        return  DomainEvent(
            name=name,
            data=data,
            ocurred=time
        )
        

    async def create_and_publish(self, name:str, data:str, ocurred:datetime|str=None)->DomainEvent:
        time = datetime.now()
        if ocurred and isinstance(ocurred, str):
            time = datetime.strptime(ocurred, "%Y-%m-%d %H:%M:%S")
            
        if ocurred and isinstance(ocurred, datetime):
            time = ocurred
            
        event =  DomainEvent(
            name=name,
            data=data,
            ocurred=time
        )
        if self.mediator:
            await self.mediator.publish(event)
        
        return event