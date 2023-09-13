from blazetelegrambot.domain.entitys.double import Double

from datetime import datetime, timedelta

def test_double():
    red_time = datetime.strptime('2023-08-09 00:00:00', "%Y-%m-%d %H:%M:%S")
    next_time = red_time + timedelta(seconds=30)
    next_two_minutes = red_time + timedelta(minutes=2)
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
    assert red_double.is_red()
    assert not red_double.is_black()
    assert not red_double.is_white()
    assert not black_double.is_red()
    assert not black_double.is_white()
    assert black_double.is_black()
    assert not white_double.is_black()
    assert not white_double.is_red()
    assert white_double.is_white()
    assert red_double.next_time() == next_time
    assert red_double.next_x_time(4) == next_two_minutes
    assert red_double.same_day(black_double)