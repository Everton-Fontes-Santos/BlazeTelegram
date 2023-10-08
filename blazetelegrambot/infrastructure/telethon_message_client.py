from ..interfaces.message_client import MessageClient

from telethon import TelegramClient

class TelethonMessage(MessageClient):
    client:TelegramClient
    
    async def send_message(self, msg: str, id_to_send: str | int) -> None:
        with self.client:
            await self.client.send_message(id_to_send, msg)