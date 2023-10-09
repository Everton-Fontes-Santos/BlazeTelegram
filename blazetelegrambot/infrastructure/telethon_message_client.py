from ..interfaces.message_client import MessageClient

from pydantic import ConfigDict
from telethon import TelegramClient

class TelethonMessage(MessageClient):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    client:TelegramClient
    counter:int = 0
    
    def add(self):
        self.counter += 1
    
    async def send_message(self, msg: str, id_to_send: str | int) -> None:
        async with self.client:
            await self.client.send_message(id_to_send, msg)
            
    async def send_message_by_count(self, msg:str, id_to_send:str|int, count:int)->None:
        if self.counter % count == 0:
            async with self.client:
                await self.client.send_message(id_to_send, msg)