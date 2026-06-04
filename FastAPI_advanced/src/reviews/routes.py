from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.db.models import User
from src.auth.dependencies import get_current_user
from .schemas import ReviewCreateModel, ReviewModel
from .service import ReviewService
from typing import List
from src.auth.dependencies import RoleChecker
from src.errors import ReviewNotFound
from src.auth.dependencies import AccessTokenBearer

role_checker = Depends(RoleChecker(["admin", "user"]))
user_review_router = APIRouter()
review_router = APIRouter()
review_service = ReviewService()


@review_router.post("/book/{book_uid}", dependencies=[role_checker])
async def add_review_to_book(
    book_uid: str,
    review_data: ReviewCreateModel,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    new_review = await review_service.add_review_to_book(
        user_email=current_user.email,
        review_data=review_data,
        book_uid=book_uid,
        session=session,
    )

    return new_review


@review_router.get(
    "/{review_uid}", response_model=ReviewModel, dependencies=[role_checker]
)
async def get_review_by_uid(
    review_uid: str, session: AsyncSession = Depends(get_session)
):
    review = await review_service.get_review_by_uid(review_uid, session)

    return review


@review_router.get(
    "/get_user_reviews/{user_id}",
    response_model=List[ReviewModel],
    dependencies=[role_checker],
)
async def get_all_user_reviews(
    user_id: str, session: AsyncSession = Depends(get_session)
):
    reviews = await review_service.get_all_user_reviews(user_id, session)

    return reviews


@review_router.delete("/{review_uid}", dependencies=[role_checker])
async def delete_review(
    review_uid: str,
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    review = await review_service.delete_review(review_uid, token_details, session)

    if review is None:
        raise ReviewNotFound()

    return review


@user_review_router.post(
    "/user/{user_uid}/review/{review_uid}", dependencies=[role_checker]
)
async def like_review_by_user(
    review_uid: str, user_uid: str, session: AsyncSession = Depends(get_session)
):
    await review_service.like_review(user_uid, review_uid, session)


@user_review_router.delete(
    "/user/{user_uid}/review/{review_uid}", dependencies=[role_checker]
)
async def unlike_review_by_user(
    review_uid: str, user_uid: str, session: AsyncSession = Depends(get_session)
):
    await review_service.unlike_review(user_uid, review_uid, session)

@user_review_router.get('/{user_uid}')
async def get_user_likes(user_uid: str, session: AsyncSession = Depends(get_session)):
    return await review_service.get_likes_by_user_id(user_uid, session)