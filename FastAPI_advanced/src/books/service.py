from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .schemas import BookCreateModel, BookUpdateModel
from src.reviews.schemas import ReviewDetailModel
from src.db.models import Book, SavedBooks, ReviewLike
from datetime import datetime
from collections import defaultdict
import uuid
from sqlalchemy import select as sa_select
from src.errors import BookNotFound

class BookService:
    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))

        result = await session.exec(statement)

        return result.all()


    async def get_user_books(self, user_uid: str, session: AsyncSession):
        statement = (
            select(Book)
            .where(Book.user_uid == user_uid)
            .order_by(desc(Book.created_at))
        )

        result = await session.exec(statement)

        return result.all()


    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)

        result = await session.exec(statement)

        book = result.first()

        return book if book is not None else None


    async def create_book(
        self, book_data: BookCreateModel, user_uid: str, session: AsyncSession
    ):
        book_data_dict = book_data.model_dump()

        new_book = Book(**book_data_dict)  # returns key value pairs

        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d"
        )

        new_book.user_uid = user_uid

        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(
        self, book_uid: str, update_data: BookUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:

            book_update_data_dict = update_data.model_dump()

            for k, v in book_update_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()

            return book_to_update

        else:
            return None

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)

            await session.commit()

            return {}
        else:
            return None


    async def get_books_with_saves(self, books: list, user_uid: str, session: AsyncSession):
        statement = await session.exec(
            select(SavedBooks).where(SavedBooks.user_uid == user_uid)
        )
        all_saved_books = statement.all()
        saved_by_user = {str(s.book_uid) for s in all_saved_books}

        saved_count = defaultdict(int)
        for s in all_saved_books:
            saved_count[str(s.book_uid)] += 1

        return [
            {
                **book.model_dump(),
                "is_saved": str(book.uid) in saved_by_user,
                "saved_count": saved_count[str(book.uid)]
            }
            for book in books
        ]
        
    
    async def get_book_review_details(self, book_uid: str, user_uid: str, session: AsyncSession):
        book = await self.get_book(book_uid, session)

        if not book:
            raise BookNotFound()
        review_uids = [uuid.UUID(str(r.uid)) for r in book.reviews]


        statement = sa_select(ReviewLike).where(ReviewLike.review_uid.in_(review_uids))
        result = await session.exec(statement)
        likes = result.scalars().all()
        
        likes_by_review = defaultdict(list)
        for like in likes:
            likes_by_review[str(like.review_uid)].append(str(like.user_uid))
            
        reviews = [
            ReviewDetailModel(
                **review.model_dump(),
                user=review.user,
                likes_count=len(likes_by_review[str(review.uid)]),
                is_liked=user_uid in likes_by_review[str(review.uid)]
            ) for review in book.reviews
        ]
        
        return {**book.model_dump(), "reviews": reviews, "tags": book.tags}