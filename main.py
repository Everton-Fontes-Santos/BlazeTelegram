from blazetelegrambot.handlers import (
    double_msg_sender, log_handler, roulette_updated
)
from blazetelegrambot.services import (
    add_double, create_strategy, transform_bet_to_msg_result, transform_bet_to_msg_signal,
    create_telegram_message_client
)
from blazetelegrambot.services.factorys import (
    color_strategys
)
from blazetelegrambot.dispatchers.MemoryDispatcher import MemoryDispatcher

import asyncio

async def main():
    #create the mediator
    mediator = MemoryDispatcher()
    log = log_handler.LogHandler()
    #register log service
    mediator.register(log)


    #create message client
    message_client_service = create_telegram_message_client.CreateTelegramMessageClient()
    message_client = await message_client_service.execute({
        'api_hash':"de909c52ddc8058bb7a47ef5e4cd73ab",
        'api_id':"10432709",
        "session_name":"efs_bot",
        'bot_token':'1973644874:AAFGExBXStuorX8KbNuyepHENuMxcnNZWj0'
    })

    strategy_creator = create_strategy.CreateStrategy(color_strategys.ColorStrategYFactorys())
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
        client=message_client
    )

    mediator.register(sender_handler)

if __name__ == '__main__':
    asyncio.run(main())