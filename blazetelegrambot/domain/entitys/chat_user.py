from pydantic import BaseModel


class ChatUser(BaseModel):
    id:int
    name:str