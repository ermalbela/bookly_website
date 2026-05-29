from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from src.db.models import Tag, Book, BookTag
from .schemas import TagCreateModel
from fastapi import HTTPException, status
from src.errors import (
    TagNotFound,
    TagAlreadyAddedToBook,
    BookNotFound,
    TagAlreadyExists,
    TagNotAssociatedToBook,
)


class TagService:

    async def get_all_tags(self, session: AsyncSession):
        result = await session.exec(select(Tag).order_by(desc(Tag.created_at)))
        return result.all()

    async def get_tag_by_uid(self, tag_uid: str, session: AsyncSession):
        result = await session.exec(select(Tag).where(Tag.uid == tag_uid))
        tag = result.first()
        if not tag:
            raise TagNotFound()
        return tag

    async def create_tag(self, tag_data: TagCreateModel, session: AsyncSession):
        existing = await session.exec(select(Tag).where(Tag.name == tag_data.name))
        if existing.first():
            raise TagAlreadyExists()

        if not tag_data.name:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag should contain a name")
        
        new_tag = Tag(name=tag_data.name)

        session.add(new_tag)
        await session.commit()
        await session.refresh(new_tag)

        return new_tag

    async def update_tag(
        self, tag_uid: str, tag_data: TagCreateModel, session: AsyncSession
    ):
        tag = await self.get_tag_by_uid(tag_uid, session)

        if tag is not None:
            tag.name = tag_data.name
            await session.commit()
            await session.refresh(tag)
            return tag

        else:
            return None

    async def delete_tag(self, tag_uid: str, session: AsyncSession):
        tag = await self.get_tag_by_uid(tag_uid, session)

        if tag is not None:

            await session.delete(tag)
            await session.commit()
            return {}
        else:
            return None

    async def add_tag_to_book(self, book_uid: str, tag_uid: str, session: AsyncSession):
        book = await session.exec(select(Book).where(Book.uid == book_uid))
        book = book.first()
        if not book:
            raise BookNotFound()

        tag = await self.get_tag_by_uid(tag_uid, session)

        existing_link = await session.exec(
            select(BookTag).where(
                BookTag.book_uid == book_uid, BookTag.tag_uid == tag_uid
            )
        )
        if existing_link.first():
            raise TagAlreadyAddedToBook()

        link = BookTag(book_uid=book_uid, tag_uid=tag_uid)
        session.add(link)
        await session.commit()
        await session.refresh(book)
        return link

    async def remove_tag_from_book(
        self, book_uid: str, tag_uid: str, session: AsyncSession
    ):
        link = await session.exec(
            select(BookTag).where(
                BookTag.book_uid == book_uid, BookTag.tag_uid == tag_uid
            )
        )
        link = link.first()
        if not link:
            raise TagNotAssociatedToBook()

        await session.delete(link)
        await session.commit()
