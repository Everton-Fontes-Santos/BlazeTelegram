from blazetelegrambot.handlers import (
    double_msg_sender, log_handler
)
from blazetelegrambot.services import (
    add_double, create_strategy, transform_bet_to_msg_result, transform_bet_to_msg_signal,
    create_telegram_message_client, roulette_checker
)
from blazetelegrambot.domain.entitys.roulette import Roulette
from blazetelegrambot.infrastructure.httpx_client import HTTPXClient
from blazetelegrambot.domain.factory.event_factory import EventFactory
from blazetelegrambot.services.factorys import (
    color_strategys
)
from blazetelegrambot.dispatchers.MemoryDispatcher import MemoryDispatcher
from blazetelegrambot.presenters.roulette_updater import RouletteUpdater
from blazetelegrambot.services.telegram_config import TelegramConfig

import asyncio

async def main():
    config = TelegramConfig()
    roulette = Roulette()
    http = HTTPXClient()
    #create the mediator
    event_factory = EventFactory()
    mediator = MemoryDispatcher()
    log = log_handler.LogHandler()
    #register log service
    mediator.register(log)

    rou_checker = roulette_checker.RouletteChecker(web_client=http)

    #create message client
    message_client_service = create_telegram_message_client.CreateTelegramMessageClient()
    message_client = await message_client_service.execute({
        "session_name":config.SESSION_NAME,
        "bot_token":config.BOT_TOKEN,
        "api_id":config.API_ID,
        "api_hash":config.API_HASH
    })

    add = add_double.AddDouble(roulette=roulette, event_factory=event_factory)


    presenter = RouletteUpdater(roulette_checker=rou_checker, add_double=add)

    strategy_creator = create_strategy.CreateStrategy(strategy_factory=color_strategys.ColorStrategYFactorys())
    #strategys to lookup
    red_strategy = await strategy_creator.execute({
        'broker':'blaze',
        'pattern':[1, 1, 1, 2, 2],
        'signal':1
    })

    black_strategy = await strategy_creator.execute({
        'broker':'blaze',
        'pattern':[2, 2, 2, 1, 1],
        'signal':2
    })

    white_strategy = await strategy_creator.execute({
        'broker':'blaze',
        'pattern':[0],
        'signal':3
    })

    sender_handler = double_msg_sender.DoubleMsgSenderHandler(
        strategys=[red_strategy, black_strategy, white_strategy],
        transform_bet_to_msg_result=transform_bet_to_msg_result.TransformBetToMsgResult(),
        transform_bet_to_msg_signal=transform_bet_to_msg_signal.TransformBetToMsgSignal(),
        client=message_client.client
    )

    sender_handler.addIds('color', config.COLOR_PAID_GROUP)
    sender_handler.addIds('white', config.WHITE_PAID_GROUP)
    
    mediator.register(sender_handler)

    await presenter.listen()
    message_client.client.client.run_until_disconnected()
    
if __name__ == '__main__':
    asyncio.run(main())