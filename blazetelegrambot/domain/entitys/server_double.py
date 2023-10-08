from pydantic import BaseModel

from datetime import datetime 


class ServerDouble(BaseModel):
    #{"id":"blRLpBo91O","created_at":"2023-08-13T02:24:02.150Z","color":2,"roll":8,"server_seed":"2e1f5b6ea10e83e51e8f5b85559a237a633954a55ce62d860d130c25b057a169"}
    id:str
    created_at:datetime
    color:int
    roll:int
    server_seed:str
    
class DoubleRecents(BaseModel):
    doubles:list[ServerDouble]