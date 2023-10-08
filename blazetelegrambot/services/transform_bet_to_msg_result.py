from ..domain.entitys.bet import Bet
from ..interfaces.service import Service, ServiceInput, ServiceOutput

from datetime import datetime, timedelta
import re
from typing import TypedDict, Literal


class Input(TypedDict):
    init_time:datetime
    start_time:datetime
    mid_time:datetime
    end_time:datetime
    signal:int
    active:bool
    broker:str
    win:str

class MsgOutPut(ServiceOutput):
    text:str
    color:Literal['color', 'white']

class TransformMsgInput(ServiceInput):
    bet:Bet

class TransformBetToMsgResult(Service):
    
    def execute(self, input: Input) -> MsgOutPut:
        input['mid_time'] = input['init_time'] if not input['mid_time'] else input['mid_time']
        bet = Bet(**input)
        
        if "GALE" in bet.win and bet.win == "":
            return
        #set the default text
        msg_text = "Método High White - Resultado do Sinal \n"
        if bet.win == "LOSS":
            msg_text += "🥊🥊🚨 LOSS! Relaxa, segue o gerenciamento seguro que na proxima vem! 🚨🥊🥊"
        elif bet.win == 'WIN':            
            msg_text += "Blaze? Tu quer pegar meu dinheiro? YOU SHALL NOT PASS! \n\n"
            msg_text += '🤑🤑🤑🧨🎁 Paaaagaaaa!!! WINZÃO!!!'
        else:
            msg_text = ''
            
        if not msg_text:
            return
        
        #check if a white bet
        if bet.signal == 0:
            #send to white group
            color = 'white'
            
        else:
            msg_text = msg_text.replace("White", "Colors")            
            color = 'color'
        
        send_msg = msg_text
        return MsgOutPut(
            text=send_msg,
            color=color
        )
        
        
    