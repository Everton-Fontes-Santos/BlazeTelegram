from ....interfaces.bet_factory import Bet, BetFactory
from ...entitys.roulette import Roulette


from datetime import timedelta


class TenMinutesWhiteFactory(BetFactory):
    broker:str = 'blaze'
    
    def create(self, roulette:Roulette)->Bet:
        last_time = roulette.last().creation_time - timedelta(seconds=roulette.last().creation_time.second, microseconds=roulette.last().creation_time.microsecond)
        start_time = last_time + timedelta(minutes=3)
        mid_time = start_time + timedelta(minutes=3)
        end_time = last_time + timedelta(minutes=10)
        
        return Bet(init_time=last_time, start_time=start_time, mid_time=mid_time, end_time=end_time, signal=0, active=True, broker=self.broker)
        