from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from sqlmodel import select, desc
from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from .schemas import ReviewCreateModel, ReviewModel
import logging
from src.errors import UserNotFound, BookNotFound

user_service = UserService()
book_service = BookService()


class ReviewService:
    async def add_review_to_book(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateModel,
        session: AsyncSession,
    ) -> Review:

        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)
            user = await user_service.get_user_by_email(
                email=user_email, session=session
            )

            new_review = Review(**review_data.model_dump())

            if not book:
                raise BookNotFound()

            if not user:
                raise UserNotFound()

            new_review.user = user
            new_review.book = book

            session.add(new_review)
            await session.commit()

            return new_review

        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong."
            )

    async def get_review_by_uid(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)

        result = await session.exec(statement)

        review = result.first()

        return review if review is not None else None

    async def get_all_user_reviews(self, user_id: str, session: AsyncSession):
        statement = (
            select(Review)
            .where(Review.user_uid == user_id)
            .order_by(desc(Review.created_at))
        )

        result = await session.exec(statement)

        return result.all()
