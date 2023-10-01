from blazetelegrambot.domain.entitys.roulette import Roulette
from blazetelegrambot.domain.entitys.double import Double
from blazetelegrambot.infrastructure.checkers.win_checker import WinChecker
from blazetelegrambot.infrastructure.signal_strategys.color_strategy import ColorStrategy
from blazetelegrambot.infrastructure.signal_strategys.roll_strategy import RollStrategy
from blazetelegrambot.domain.factory.bets.single_red import SingleRedFactory
from blazetelegrambot.domain.factory.bets.ten_white import TenMinutesWhiteFactory
from blazetelegrambot.domain.factory.bets.single_black import SingleBlackFactory

async def test_strategy_check_pattern():
    doubles = [
        Double(color=1, roll=1, creation_time='2023-08-04T09:30:00', broker='blaze'),
        Double(color=1, roll=3, creation_time='2023-08-04T09:30:30', broker='blaze'),
        Double(color=1, roll=4, creation_time='2023-08-04T09:31:00', broker='blaze'),
        Double(color=2, roll=9, creation_time='2023-08-04T09:31:30', broker='blaze'),
        Double(color=2, roll=8, creation_time='2023-08-04T09:32:00', broker='blaze'),
    ]
    roulette = Roulette()
    roulette.add(*doubles)
    strategy = ColorStrategy(signal=2, pattern=[1,1,1,2,2], checker=WinChecker())
    assert strategy.check_pattern(roulette) == True
    
    
    doubles = [
        Double(color=1, roll=1, creation_time='2023-08-04T09:30:00', broker='blaze'),
        Double(color=1, roll=3, creation_time='2023-08-04T09:30:30', broker='blaze'),
        Double(color=1, roll=4, creation_time='2023-08-04T09:31:00', broker='blaze'),
        Double(color=1, roll=9, creation_time='2023-08-04T09:31:30', broker='blaze'),
        Double(color=2, roll=8, creation_time='2023-08-04T09:32:00', broker='blaze'),
    ]
    roulette.add(*doubles)
    assert strategy.check_pattern(roulette) == False
    
    doubles = [
        Double(color=1, roll=1, creation_time='2023-08-04T09:30:00', broker='blaze'),
        Double(color=1, roll=3, creation_time='2023-08-04T09:30:30', broker='blaze'),
        Double(color=2, roll=4, creation_time='2023-08-04T09:31:00', broker='blaze'),
        Double(color=2, roll=9, creation_time='2023-08-04T09:31:30', broker='blaze'),
        Double(color=2, roll=8, creation_time='2023-08-04T09:32:00', broker='blaze'),
    ]
    roulette.add(*doubles)
    strategy = RollStrategy(signal=2, pattern=[1,3,4,9,8], read_type="roll", checker=WinChecker())
    assert strategy.check_pattern(roulette) == True
    
    doubles = [
        Double(color=1, roll=1, creation_time='2023-08-04T09:30:00', broker='blaze'),
        Double(color=1, roll=3, creation_time='2023-08-04T09:30:30', broker='blaze'),
        Double(color=2, roll=4, creation_time='2023-08-04T09:31:00', broker='blaze'),
        Double(color=0, roll=0, creation_time='2023-08-04T09:31:30', broker='blaze'),
        Double(color=1, roll=5, creation_time='2023-08-04T09:32:00', broker='blaze'),
    ]
    roulette.add(*doubles)
    strategy = RollStrategy(signal=2, pattern=[[0, 5]], read_type="roll", checker=WinChecker())
    assert strategy.check_pattern(roulette) == True
    

async def test_strategy_check_create_bet():
    doubles = [
        Double(color=1, roll=1, creation_time='2023-08-04T09:30:00', broker='blaze'),
        Double(color=1, roll=3, creation_time='2023-08-04T09:30:30', broker='blaze'),
        Double(color=1, roll=4, creation_time='2023-08-04T09:31:00', broker='blaze'),
        Double(color=2, roll=9, creation_time='2023-08-04T09:31:30', broker='blaze'),
        Double(color=2, roll=8, creation_time='2023-08-04T09:32:00', broker='blaze'),
    ]
    roulette = Roulette()
    roulette.add(*doubles)
    factory = SingleBlackFactory()
    strategy = ColorStrategy(signal=2, pattern=[1,1,1,2,2], bet_factory=factory, checker=WinChecker())
    strategy.check(roulette)
    assert strategy.actual_bet.signal == 2
    
async def test_strategy_check_create_bet_red():
    doubles = [
        Double(color=2, roll=8, creation_time='2023-08-04T09:30:00', broker='blaze'),
        Double(color=2, roll=9, creation_time='2023-08-04T09:30:30', broker='blaze'),
        Double(color=2, roll=11, creation_time='2023-08-04T09:31:00', broker='blaze'),
        Double(color=1, roll=9, creation_time='2023-08-04T09:31:30', broker='blaze'),
        Double(color=1, roll=8, creation_time='2023-08-04T09:32:00', broker='blaze'),
    ]
    roulette = Roulette()
    roulette.add(*doubles)
    factory = SingleRedFactory()
    strategy = ColorStrategy(signal=1, pattern=[2,2,2,1,1], bet_factory=factory, checker=WinChecker())
    strategy.check(roulette)
    assert strategy.actual_bet.signal == 1
    
async def test_strategy_check_create_bet_white_ten_minutes():
    doubles = [
        Double(color=0, roll=0, creation_time='2023-08-04T09:32:00', broker='blaze'),
    ]
    roulette = Roulette()
    roulette.add(*doubles)
    factory = TenMinutesWhiteFactory()
    strategy = ColorStrategy(signal=0, pattern=[0], bet_factory=factory, checker=WinChecker())
    strategy.check(roulette)
    assert strategy.actual_bet.signal == 0
    assert strategy.actual_bet.start_time.minute == 35
    assert strategy.actual_bet.end_time.minute == 42
    
    #no signal
    roulette.add(Double(color=0, roll=0, creation_time='2023-08-04T09:35:00', broker='blaze'))
    strategy.check(roulette)
    assert strategy.actual_bet.start_time.minute == 35
    assert strategy.actual_bet.end_time.minute == 42
    
    roulette.add(Double(color=0, roll=0, creation_time='2023-08-04T09:37:00', broker='blaze'))
    strategy.check(roulette)
    assert strategy.actual_bet.start_time.minute == 35
    assert strategy.actual_bet.end_time.minute == 42  
    
    #signal2
    roulette.add(Double(color=0, roll=0, creation_time='2023-08-04T09:43:00', broker='blaze'))
    strategy.check(roulette)
    assert strategy.actual_bet.start_time.minute == 46
    assert strategy.actual_bet.end_time.minute == 53
    
    roulette.add(Double(color=0, roll=0, creation_time='2023-08-04T09:48:00', broker='blaze'))
    strategy.check(roulette)
    assert strategy.actual_bet.start_time.minute == 46
    assert strategy.actual_bet.end_time.minute == 53
    
    roulette.add(Double(color=0, roll=0, creation_time='2023-08-04T09:53:00', broker='blaze'))
    strategy.check(roulette)
    assert strategy.actual_bet.start_time.minute == 46
    assert strategy.actual_bet.end_time.minute == 53
    
    roulette.add(Double(color=0, roll=0, creation_time='2023-08-04T09:53:30', broker='blaze'))
    strategy.check(roulette)
    assert strategy.actual_bet.start_time.minute == 46
    assert strategy.actual_bet.end_time.minute == 53