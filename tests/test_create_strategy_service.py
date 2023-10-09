from blazetelegrambot.services.create_strategy import CreateStrategy, InputDict
from blazetelegrambot.services.factorys import (
    color_and_roll_strategys_factory, color_strategys, roll_strategys_factory
)

async def test_create_strategy_service():
    red = CreateStrategy(strategy_factory=color_strategys.ColorStrategYFactorys())
    black = CreateStrategy(strategy_factory=color_strategys.ColorStrategYFactorys())
    white = CreateStrategy(strategy_factory=color_strategys.ColorStrategYFactorys())
    white_ten = CreateStrategy(strategy_factory=color_strategys.ColorStrategYFactorys())
    roll = CreateStrategy(strategy_factory=roll_strategys_factory.RollStrategYFactorys())
    _any = CreateStrategy(strategy_factory=color_and_roll_strategys_factory.ColorAndRollStrategYFactorys())
    
    input:InputDict = {
        'signal':1,
        'broker':'blaze',
        'pattern':['red', 'red', 'red', 'black', 'black']
    }
    
    red_strat = await red.execute(input)
    red_strat = red_strat.strategy
    assert red_strat.actual_bet == None
    assert red_strat.pattern == input['pattern']
    assert red_strat.signal == input['signal']
    
    
    input['signal'] = 2
    black_strat = await black.execute(input)
    black_strat = black_strat.strategy
    assert black_strat.actual_bet == None
    assert black_strat.pattern == input['pattern']
    assert black_strat.signal == input['signal']
    
    input['signal'] = 3
    white_strat = await white_ten.execute(input)
    white_strat = white_strat.strategy
    assert white_strat.actual_bet == None
    assert white_strat.pattern == input['pattern']
    assert white_strat.signal == 0
    
    input['signal'] = 0
    white_strat = await white.execute(input)
    white_strat = white_strat.strategy
    assert white_strat.actual_bet == None
    assert white_strat.pattern == input['pattern']
    assert white_strat.signal == 0