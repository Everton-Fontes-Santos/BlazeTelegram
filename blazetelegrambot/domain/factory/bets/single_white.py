from ....interfaces.bet_factory import Bet, BetFactory
from ...entitys.roulette import Roulette


from datetime import timedelta


class SingleWhiteFactory(BetFactory):
    broker:str = 'blaze'
    
    def create(self, roulette:Roulette)->Bet:
        last_time = roulette.last().creation_time
        end_time = last_time + timedelta(seconds=90)
        
        return Bet(init_time=last_time, start_time=last_time, end_time=end_time, signal=0, active=True, broker=self.broker)
        