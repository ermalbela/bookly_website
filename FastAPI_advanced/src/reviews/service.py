from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from sqlmodel import select, desc
from src.db.models import Review, User, ReviewLike
from src.auth.service import UserService
from src.books.service import BookService
from .schemas import ReviewCreateModel, ReviewModel
import logging
from src.errors import UserNotFound, BookNotFound
from sqlalchemy.exc import IntegrityError

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

        book = await book_service.get_book(book_uid=book_uid, session=session)
        user = await user_service.get_user_by_email(email=user_email, session=session)

        new_review = Review(**review_data.model_dump())

        if not book:
            raise BookNotFound()

        if not user:
            raise UserNotFound()

        new_review.user = user
        new_review.book = book

        try:
            session.add(new_review)
            await session.commit()
        except IntegrityError:
            await session.rollback()  # if this line is missing the current session becomes unusable.
            raise HTTPException(
                detail="You have already reviewed this book.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        return new_review

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

    async def delete_review(
        self, review_uid: str, token_details: dict, session: AsyncSession
    ):
        review_to_delete = await self.get_review_by_uid(review_uid, session)

        if review_to_delete is None:
            return None
        
        print("TOKEN DETAILS???????????????//" , token_details)
        user_role = token_details["user"]["role"]
        user_uid = token_details["user"]["user_uid"]

        if user_role == "admin" or user_uid == str(review_to_delete.user_uid):
            await session.delete(review_to_delete)

            await session.commit()

            return {}

        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this review.",
            )

    async def get_likes_by_user_id(self, user_uid: str, session: AsyncSession):
        
        likes = await session.exec(select(ReviewLike).where(ReviewLike.user_uid == user_uid))
        likes = likes.all()

        return likes if likes else None


    async def like_review(self, user_uid: str, review_uid: str, session: AsyncSession):
        user = await session.exec(select(User).where(User.uid == user_uid))
        user = user.first()
        if not user:
            raise UserNotFound()

        review = await self.get_review_by_uid(review_uid, session)

        existing_like = await session.exec(
            select(ReviewLike).where(
                ReviewLike.user_uid == user_uid, ReviewLike.review_uid == review_uid
            )
        )

        if existing_like.first():
            raise HTTPException(
                detail="User has already liked this review.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        like = ReviewLike(user_uid=user_uid, review_uid=review_uid)

        session.add(like)
        await session.commit()
        await session.refresh(review)

        return like

    async def unlike_review(
        self, user_uid: str, review_uid: str, session: AsyncSession
    ):
        like = await session.exec(
            select(ReviewLike).where(
                ReviewLike.user_uid == user_uid, ReviewLike.review_uid == review_uid
            )
        )

        like = like.first()

        if not like:
            raise HTTPException(
                detail="User hasnt liked this review yet.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        await session.delete(like)
        await session.commit()
