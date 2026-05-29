from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import TagService
from .schemas import TagCreateModel, TagModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from typing import List 
from src.errors import TagNotFound


book_tag_router = APIRouter()
tag_router = APIRouter()
tag_service = TagService()

access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(["admin", "user"]))


@tag_router.get("/get_all_tags", response_model=List[TagModel], dependencies=[role_checker])
async def get_all_tags(
    session: AsyncSession = Depends(get_session),
    token_restriction: dict = Depends(access_token_bearer),
):
    return await tag_service.get_all_tags(session)


@tag_router.post("/create_tag", dependencies=[role_checker])
async def create_tag(
    tag_data: TagCreateModel,
    session: AsyncSession = Depends(get_session),
    token_restriction: dict = Depends(access_token_bearer),
):
    return await tag_service.create_tag(tag_data, session)


@tag_router.get("/{tag_uid}", response_model=TagModel, dependencies=[role_checker])
async def get_tag(
    tag_uid: str,
    session: AsyncSession = Depends(get_session),
    token_restriction: dict = Depends(access_token_bearer),
):
    return await tag_service.get_tag_by_uid(tag_uid, session)


@tag_router.patch("/edit_tag/{tag_uid}", response_model=TagModel, dependencies=[role_checker])
async def update_tag(
    tag_uid: str,
    tag_data: TagCreateModel,
    session: AsyncSession = Depends(get_session),
    token_restriction: dict = Depends(access_token_bearer),
):
    return await tag_service.update_tag(tag_uid, tag_data, session)


@tag_router.delete(
    "/remove_tag/{tag_uid}",status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_tag(
    tag_uid: str,
    session: AsyncSession = Depends(get_session),
    token_restriction: dict = Depends(access_token_bearer),
):
    tag_to_delete = await tag_service.delete_tag(tag_uid, session)
    
    if tag_to_delete is None:
        raise TagNotFound()
    else:
        return None

@book_tag_router.post("/book/{book_uid}/tag/{tag_uid}", dependencies=[role_checker])
async def add_tag_to_book(
    book_uid: str,
    tag_uid: str,
    session: AsyncSession = Depends(get_session),
    token_restriction: dict = Depends(access_token_bearer),
):
    return await tag_service.add_tag_to_book(book_uid, tag_uid, session)


@book_tag_router.delete(
    "/book/{book_uid}/tag/{tag_uid}", status_code=204, dependencies=[role_checker]
)
async def remove_tag_from_book(
    book_uid: str,
    tag_uid: str,
    session: AsyncSession = Depends(get_session),
    token_restriction: dict = Depends(access_token_bearer),
):
    await tag_service.remove_tag_from_book(book_uid, tag_uid, session)
