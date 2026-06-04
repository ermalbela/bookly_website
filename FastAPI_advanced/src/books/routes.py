from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from src.db.models import ReviewLike
from sqlalchemy import select as sa_select
from src.books.service import BookService
from .schemas import Book, BookUpdateModel, BookCreateModel, BookDetailModel, ReviewDetailModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.db.main import get_session
from src.errors import BookNotFound
from collections import defaultdict
import uuid

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))
admin_checker = Depends(RoleChecker(["admin"]))


@book_router.get("/", response_model=List[BookDetailModel], dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_all_books(session)
    return books


@book_router.get("/user/{user_uid}", response_model=List[Book], dependencies=[role_checker])
async def get_user_book_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    books = await book_service.get_user_books(user_uid, session)
    
    return books


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[admin_checker],
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_id, session)

    return new_book


@book_router.get("/{book_uid}", response_model=BookDetailModel, dependencies=[role_checker])
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    book = await book_service.get_book(book_uid, session)

    if not book:
        raise BookNotFound()

    current_user_uid = token_details["user"]["user_uid"]
    review_uids = [uuid.UUID(str(r.uid)) for r in book.reviews]


    stmt = sa_select(ReviewLike).where(ReviewLike.review_uid.in_(review_uids))
    result = await session.exec(stmt)
    likes = result.scalars().all()
    
    likes_by_review = defaultdict(list)
    for like in likes:
        likes_by_review[str(like.review_uid)].append(str(like.user_uid))
        
    reviews = [
        ReviewDetailModel(
            **review.model_dump(),
            user=review.user,
            likes_count=len(likes_by_review[str(review.uid)]),
            is_liked=current_user_uid in likes_by_review[str(review.uid)]
        ) for review in book.reviews
    ]
    
    return {**book.model_dump(), "reviews": reviews, "tags": book.tags}

@book_router.patch("/{book_uid}", response_model=Book, dependencies=[admin_checker])
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
) -> dict:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        raise BookNotFound()
    else:
        return updated_book


@book_router.delete(
    "/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise BookNotFound()
    else:
        return None
