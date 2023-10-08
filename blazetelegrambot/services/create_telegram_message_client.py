from typing import Any
from ..interfaces.service import Service, ServiceOutput, ServiceInput
from ..infrastructure.telethon_message_client import TelethonMessage, TelegramClient
from ..handlers.log_handler import logger

class Input(ServiceInput):
    session_name:str
    bot_token:str
    api_id:str
    api_hash:str

class Output(ServiceOutput):
    client:TelethonMessage


class CreateTelegramMessageClient(Service):
    
    async def execute(self, input: dict[str, Any]):
        _input = Input(**input)
        client = TelegramClient(_input.session_name, _input.api_id, _input.api_hash)
        await client.start(bot_token=_input.bot_token)
        
        message = TelethonMessage(client=client)
        return Output(client=message)