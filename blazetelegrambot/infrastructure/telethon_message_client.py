from ..interfaces.message_client import MessageClient

from pydantic import ConfigDict
from telethon import TelegramClient

class TelethonMessage(MessageClient):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    client:TelegramClient
    
    async def send_message(self, msg: str, id_to_send: str | int) -> None:
        with self.client:
            await self.client.send_message(id_to_send, msg)