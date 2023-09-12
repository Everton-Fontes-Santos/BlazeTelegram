from ..interfaces.base_event import DomainEvent
from ..interfaces.handler import Handler

import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("rich")


class LogHandler(Handler):
    name:str = 'log'
    
    async def handle(self, event: DomainEvent) -> None:
        
        msg = f'Event: {event.name} - ocurred {event.ocurred}\n'
        msg += f'Payload: {event.data}'
        logger.info(
            msg
        )