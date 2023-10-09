from blazetelegrambot.services.transform_bet_to_msg_signal import TransformBetToMsgSignal
from blazetelegrambot.services.transform_bet_to_msg_result import TransformBetToMsgResult
from blazetelegrambot.handlers.double_msg_sender import DoubleMsgSenderHandler, DomainEvent
from blazetelegrambot.interfaces.message_client import MessageClient
from blazetelegrambot.domain.entitys.bet import Bet
from blazetelegrambot.domain.entitys.roulette import Roulette
from blazetelegrambot.domain.entitys.double import Double
from blazetelegrambot.services.factorys.color_strategys import ColorStrategYFactorys

class MockMessage(MessageClient):
    msgs:list[tuple] = []
    
    def __len__(self)->int:
        return len(self.msgs)
    
    async def send_message(self, msg: str, id_to_send: str | int) -> None:
        self.msgs.append(
            ( id_to_send , msg )
        )
    
    async def send_message_by_count(self, msg: str, id_to_send: str | int, count: int) -> None:
        if self.counter % count == 0:
            self.msgs.append(
            ( id_to_send , msg )
        )
            
        
        
async def test_signal_sender():
    client = MockMessage()
    transform = TransformBetToMsgSignal()
    transform_result = TransformBetToMsgResult()
    bet = Bet(
        signal=1,
        start_time='2023-10-09 09:59:30',
        init_time='2023-10-09 09:59:30',
        end_time='2023-10-09 10:00:30',
        broker='blaze'
    )
    white_bet = Bet(
        signal=0,
        start_time='2023-10-09 10:03:00',
        init_time='2023-10-09 10:03:00',
        mid_time='2023-10-09 10:06:00',
        end_time='2023-10-09 10:10:00',
        broker='blaze'
    )
    roullete = Roulette()
    roullete.add(
        Double(color=1, roll=1, creation_time='2023-10-09 09:57:30', broker='blaze'),
        Double(color=1, roll=3, creation_time='2023-10-09 09:58:00', broker='blaze'),
        Double(color=1, roll=5, creation_time='2023-10-09 09:58:30', broker='blaze'),
        Double(color=2, roll=8, creation_time='2023-10-09 09:59:00', broker='blaze'),
        Double(color=2, roll=10, creation_time='2023-10-09 09:59:30', broker='blaze')
    )
    
    msg = transform.execute(bet.model_dump())
    assert msg.color == 'color'
    assert '' != msg.text
    
    
    white_msg = transform.execute(white_bet.model_dump())
    assert white_msg.color == 'white'
    assert '' != white_msg.text
    
    
    event = DomainEvent(name='roullete-updated', data=roullete.model_dump_json())
    red_strategy = ColorStrategYFactorys().create(signal=1, pattern=[1, 1, 1, 2, 2], broker='blaze')
    white_strategy = ColorStrategYFactorys().create(signal=3, pattern=[0], broker='blaze')
    handler = DoubleMsgSenderHandler(
        client=client,
        strategys=[red_strategy, white_strategy],
        transform_bet_to_msg_signal=transform,
        transform_bet_to_msg_result=transform_result
    )
    id = 123
    
    handler.addIds('color', id)
    handler.addIds('white', id)
    
    assert len(handler.send_to) == 2

    await handler.handle(event)
    
    assert len(client) == 1
    id1, msg1 = client.msgs[0]
    assert id1 == id
    assert msg1 == msg.text
    
    
    roullete.add(Double(color=0, roll=0, creation_time='2023-10-09 10:00:00', broker='blaze'))
    event = DomainEvent(name='roullete-updated', data=roullete.model_dump_json())
    await handler.handle(event)
    
    assert len(client) == 2
    id2, msg2 = client.msgs[1]
    assert id2 == id
    assert msg2 == white_msg.text
    
    roullete.add(Double(color=1, roll=1, creation_time='2023-10-09 10:00:30', broker='blaze'))
    event = DomainEvent(name='roullete-updated', data=roullete.model_dump_json())
    await handler.handle(event)
    
    
    bet.win = 'WIN'
    result_red = transform_result.execute(bet.model_dump())
    assert len(client) == 3
    id3, msg3 = client.msgs[2]
    assert id3 == id
    assert msg3 == result_red.text
    
    
    roullete.add(Double(color=1, roll=1, creation_time='2023-10-09 10:10:30', broker='blaze'))
    event = DomainEvent(name='roullete-updated', data=roullete.model_dump_json())
    await handler.handle(event)
    
    white_bet.win = 'LOSS'
    result_white = transform_result.execute(white_bet.model_dump())
    assert len(client) == 4
    id4, msg4 = client.msgs[3]
    assert id4 == id
    assert msg4 == result_white.text