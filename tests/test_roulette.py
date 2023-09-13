from blazetelegrambot.domain.entitys.roulette import Roulette, Double

from datetime import datetime


def test_roulette():
    red_time = datetime.strptime('2023-08-09 00:00:00', "%Y-%m-%d %H:%M:%S")
    red_double = Double(
        color=1,
        roll=1,
        creation_time=red_time,
        broker='blaze'
    )
    black_double = Double(
        color=2,
        roll=8,
        creation_time='2023-08-09 00:00:30',
        broker='blaze'
    )
    white_double = Double(
        color=0,
        roll=0,
        creation_time='2023-08-09 00:01:00',
        broker='blaze'
    )
    roulette = Roulette()
    roulette.add(red_double)
    assert len(roulette) == 1
    roulette.add(red_double)
    assert len(roulette) == 2
    roulette.add(white_double)
    assert len(roulette) == 3
    roulette.add(black_double)
    assert len(roulette) == 4
    roulette.add(black_double)
    assert len(roulette) == 5
    assert roulette.last() == black_double
    assert roulette.first() == red_double
    assert roulette.last_n(3) == [white_double, black_double, black_double]