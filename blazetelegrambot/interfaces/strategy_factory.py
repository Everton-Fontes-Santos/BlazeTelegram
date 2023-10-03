from pydantic import BaseModel
from typing import Literal
from .signal_strategy import SignalStrategy, Pattern


from datetime import datetime

class StrategyFactory(BaseModel):
    """The Event Factory its a factory thats broke the SRP,
    but will be very usefull in the aplication,
    he will be able to just create a event, and create a event and send to handlers

    Returns:
        SignalStrategy: The strategy of type choosed
    """
    def create(self, signal:Literal[0,1,2,3], pattern:Pattern, broker:str)->SignalStrategy:
        ...
    