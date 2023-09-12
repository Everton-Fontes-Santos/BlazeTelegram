from ..interfaces.base_event import DomainEvent
from ..interfaces.dispatcher import Dispatcher
from ..interfaces.handler import Handler


class MemoryDispatcher(Dispatcher):
    """This Dispatcher its a implementation for
    running on direct machine with no microservices.
    Using modules in the aplication.
    
    Args:
        Dispatcher (_type_): No args its needed
        
    """
    handlers:dict[str, list[Handler]] = {}
    
    def register(self, handler: Handler) -> None:
        if not handler.name in self.handlers:
            self.handlers[handler.name] = [handler]
            return
            
        if handler in self.handlers[handler.name]:
            return 
        
        self.handlers[handler.name].append(handler)
        
    async def publish(self, event: DomainEvent) -> None:
        #send to respective handlers
        for event_name, handlers in self.handlers.items():
            if event.name == event_name:
                for handler in handlers:
                    await handler.handle(event)
        
        #send to loggers handlers
        if 'log' in self.handlers.keys():
            for handler in self.handlers['log']:
                await handler.handle(event)