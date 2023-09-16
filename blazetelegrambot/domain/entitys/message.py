from pydantic import BaseModel
from datetime import datetime


class BaseMessage(BaseModel):
    group:int
    sender_name:str|None
    occured:datetime
    msg:str