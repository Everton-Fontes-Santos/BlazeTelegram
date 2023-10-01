from blazetelegrambot.infrastructure.checkers.win_checker import WinChecker
from blazetelegrambot.domain.entitys.bet import Bet
from blazetelegrambot.domain.entitys.double import Double


async def test_checker():
    bet = Bet(
        init_time="2023-08-03T11:00:00",
        start_time="2023-08-03T11:00:00",
        end_time="2023-08-03T11:01:30",
        signal=1,
        broker="la",
    )
    checker = WinChecker()
    win_double = Double(
        color=1,
        roll=2,
        creation_time="2023-08-03T11:00:30",
        broker="la"
    )
    
    first_double = Double(
        color=2,
        roll=2,
        creation_time="2023-08-03T11:00:30",
        broker="la"
    )
    
    second_double = Double(
        color=2,
        roll=2,
        creation_time="2023-08-03T11:01:00",
        broker="la"
    )
    
    third_double = Double(
        color=2,
        roll=2,
        creation_time="2023-08-03T11:01:30",
        broker="la"
    )
    
    checker.check(bet, win_double)
    assert bet.win == "WIN"
     
    bet.win = ''
    checker.check(bet, first_double)
    assert bet.win == "GALE 1"
    
    checker.check(bet, second_double)
    assert bet.win == "GALE 2"
    
    checker.check(bet, third_double)
    assert bet.win == "LOSS"