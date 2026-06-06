from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Optional
from datetime import datetime
import uuid

class ReviewUser(BaseModel):
    username: str
    avatar_url: str

    model_config = ConfigDict(from_attributes=True)

class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(lt=6)
    review_text: str
    user_uid: Optional[uuid.UUID] = None
    book_uid: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime = None    
    user: Optional[ReviewUser] = None
    
    model_config = ConfigDict(from_attributes=True)

    
class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=6)
    review_text: str
    
    
class ReviewDetailModel(ReviewModel):
    likes_count: int = 0
    is_liked: bool = False
    