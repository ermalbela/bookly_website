from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.db.models import User, Book, SavedBooks
from .schemas import UserCreateModel
from .utils import generate_password_hash
from src.errors import UserNotFound, BookNotFound
from fastapi import HTTPException, status


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        
        result = await session.exec(statement)
        
        user = result.first()
        
        return user
    
    
    async def get_user_by_id(self, user_uid: str, session: AsyncSession):
        statement = select(User).where(User.uid == user_uid)
        
        result = await session.exec(statement)
        
        user = result.first()
        
        return user
    
    
    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        
        return True if user is not None else False
    
    
    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        
        new_user = User(
            **user_data_dict
        )
        
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        new_user.role = "user"
        
        session.add(new_user)
        
        await session.commit()
        
        return new_user
    
    
    async def update_user(self, user: User, user_data: dict, session: AsyncSession):
        for k, v in user_data.items():
            setattr(user, k, v)
            
        await session.commit()
        
        return user
    
    
    async def update_avatar_url(self, avatar_url: str, user_email: str, session: AsyncSession):
        user = await self.get_user_by_email(user_email, session)
        
        if not user:
            return None
        
        user.avatar_url = avatar_url
        
        await session.commit()
        await session.refresh(user)
        
        return user
    
    
    async def save_book(self, user_uid: str, book_uid: str, session: AsyncSession):
        user = await self.get_user_by_id(user_uid, session)
        
        if not user:
            raise UserNotFound()
        
        book = await session.exec(select(Book).where(Book.uid == book_uid))
        
        if not book:
            raise BookNotFound()
        
        existing_save = await session.exec(
            select(SavedBooks).where(SavedBooks.user_uid == user_uid, SavedBooks.book_uid == book_uid))
        
        if existing_save.first():
            raise HTTPException(
                detail="User already saved this book!",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        
        saved_book = SavedBooks(book_uid=book_uid, user_uid=user_uid)
        
        session.add(saved_book)
        await session.commit()
        await session.refresh(user)
        
        return saved_book
    
    
    async def unsave_book(self, user_uid: str, book_uid: str, session: AsyncSession):
        saved_book = await session.exec(
            select(SavedBooks).where(
                SavedBooks.user_uid == user_uid, SavedBooks.book_uid == book_uid
                )
            )
        
        saved_book = saved_book.first()
        
        if not saved_book:
            raise HTTPException(
                detail="User didnt save this book yet!",
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        await session.delete(saved_book)
        await session.commit()