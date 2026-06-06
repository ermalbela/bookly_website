from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from src.books.schemas import Book, BookSavesModel
from src.reviews.schemas import ReviewModel, ReviewDetailModel


class UserCreateModel(BaseModel):
    username: str = Field(max_length=12)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    
    
class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime
    avatar_url: str
    role: str

    
class UserBooksModel(UserModel):
    books: List[Book]
    reviews: List[ReviewModel]


class UserProfileModel(BaseModel):
    saved_books: List[BookSavesModel]
    reviews: List[ReviewDetailModel]
    liked_reviews: List[ReviewDetailModel]
    

class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class EmailModel(BaseModel):
    addresses: List[str]
    
    
class PasswordResetRequestModel(BaseModel):
    email: str
    

class PasswordResetConfirmModel(BaseModel):
    new_password: str
    confirm_new_password: str