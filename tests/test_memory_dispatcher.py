from blazetelegrambot.dispatchers.MemoryDispatcher import MemoryDispatcher
from blazetelegrambot.interfaces.base_event import DomainEvent
from blazetelegrambot.interfaces.handler import Handler, DomainEvent
from blazetelegrambot.domain.factory.event_factory import EventFactory

class MochHandler(Handler):
    name:str = 'mock'
    events:list[DomainEvent] = []
    handed:int = 0
    
    async def handle(self, event: DomainEvent) -> None:
        self.events.append(event)
        self.handed += 1

    def count(self)->int:
        return len(self.events)
    
async def test_memory_dispatcher_register():
    dispatcher = MemoryDispatcher()
    handler = MochHandler()
    dispatcher.register(handler=handler)
    factory = EventFactory(mediator=dispatcher)
    event = factory.create(
        name='mock',
        ocurred='2023-08-12 09:50:00',
        data='hello mock'
    )
    
    await dispatcher.publish(event)
    
    assert len(dispatcher.handlers) == 1
    assert dispatcher.handlers['mock'][0] == handler
    assert handler.count() == 1
    assert handler.handed == 1
    
    await factory.create_and_publish(
        name='mock',
        ocurred='2023-08-12 09:50:00',
        data='hello mock'
    )
    
    assert handler.count() == 2
    assert handler.handed == 2