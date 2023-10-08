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

class TransformBetToMsgSignal(Service):
    
    def execute(self, input: Input) -> MsgOutPut:
        input['mid_time'] = input['init_time'] if not input['mid_time'] else input['mid_time']
        bet = Bet(**input)
        
        return self.transform_bet_in_message(bet)    
    
    
    def process_white_time(self, occured:datetime, msg):
        _msg = ''
        minutes = re.findall(r'[0-9]{2}', msg)
        hour = occured - timedelta(hours=3)
        for idx, minute in enumerate(minutes):
            
            if idx > 0 and int(minutes[idx-1]) > int(minute):
                hour = hour + timedelta(hours=1)
            
            time = hour.strftime("%H:%M:%S")
            _msg += time[:3] + minute + ":00⚪\n"

        return _msg
    
    def transform_bet_in_message(self, bet:Bet)->str:
        
        #check if a white bet
        if bet.signal == 0:
            #send to white group
            start = f'{bet.start_time.minute}' if bet.start_time.minute > 9 else f'0{bet.start_time.minute}'
            mid = f'{bet.mid_time.minute}' if bet.mid_time.minute > 9 else f'0{bet.mid_time.minute}'
            end = f'{bet.end_time.minute}' if bet.end_time.minute > 9 else f'0{bet.end_time.minute}'
            msg_text = f'{start} {mid} {end}'


            msg = self.process_white_time(bet.start_time, msg_text)
            if msg:
                send_msg = "Método High White - Sinais de Branco \n\n" 
                send_msg += msg
                send_msg += f'\nTenha Gerenciamento consistente! Bora Alavancar !'
                color = 'white'
        else:
            
            signal = "🔴" if bet.signal == 1 else "⚫"
            msg_text = "Método High Colors - Sinais Coloridos! \n\n"
            msg_text += f'{bet.start_time.strftime("%H:%M:%S")} -> {signal}'
            msg_text += '\n Usar até 2 Gales!\n\n'
            msg_text += f'Tenha Gerenciamento consistente! Bora Alavancar !'
            
            send_msg = msg_text
            color = 'color'
        
        return MsgOutPut(
            text=send_msg,
            color=color
        )
        
