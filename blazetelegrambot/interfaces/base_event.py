from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Optional
import uuid


class DomainEvent(BaseModel):
    id: Optional[str] = Field(default=str(uuid.uuid4()))
    name:str
    ocurred:datetime = Field(datetime.now())
    data:str