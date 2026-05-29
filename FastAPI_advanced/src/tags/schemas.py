from pydantic import BaseModel
from datetime import datetime
import uuid


class TagCreateModel(BaseModel):
    name: str
    
    
class TagModel(BaseModel):
    uid: uuid.UUID
    name: str
    created_at: datetime