from pydantic import BaseModel

from ...interfaces.signal_strategy import SignalStrategy


from datetime import datetime

class StrategyFactory(BaseModel):
    """The Event Factory its a factory thats broke the SRP,
    but will be very usefull in the aplication,
    he will be able to just create a event, and create a event and send to handlers

    Returns:
        SignalStrategy: The strategy of type choosed
    """
    

    @staticmethod
    def create(strategy_type:str)->SignalStrategy:
        ...
        