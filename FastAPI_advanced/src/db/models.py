from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import ForeignKey, UniqueConstraint
import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
from typing import List, Optional


class BookTag(SQLModel, table=True):
    __tablename__ = "book_tags"

    book_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, ForeignKey("books.uid", ondelete="CASCADE"), primary_key=True, nullable=False
        )
    )
    tag_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, ForeignKey("tags.uid", ondelete="CASCADE"), primary_key=True, nullable=False
        )
    )


class ReviewLike(SQLModel, table=True):
    __tablename__ = "review_likes"
    
    review_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, ForeignKey("reviews.uid", ondelete="CASCADE"), primary_key=True, nullable=False
        )
    )
    user_uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, ForeignKey("users.uid", ondelete="CASCADE"), primary_key=True, nullable=False
        )
    )


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        back_populates="tags",
        link_model=BookTag,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self):
        return f"<Tag {self.name}>"


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    avatar_url: Optional[str] = Field(
        default="https://res-console.cloudinary.com/dt4opkzr5/thumbnails/transform/v1/image/upload/Y19maWxsLGhfMjAwLHdfMjAw/v1/bWFuX2xwcnNydQ==/template_primary",
        sa_column=Column(
            pg.VARCHAR,
            nullable=True,
            default="https://res-console.cloudinary.com/dt4opkzr5/thumbnails/transform/v1/image/upload/Y19maWxsLGhfMjAwLHdfMjAw/v1/bWFuX2xwcnNydQ==/template_primary",
        ),
    )
    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
    liked_reviews: List["Review"] = Relationship(
        back_populates="liked_by",
        link_model=ReviewLike,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(
        sa_column=Column(
            pg.UUID, ForeignKey("users.uid", ondelete="SET NULL"), nullable=True
        )
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(
        back_populates="books"
    )  # field that allows us to access the user that added this book
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )
    tags: List[Tag] = Relationship(
        back_populates="books",
        link_model=BookTag,
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    __table_args__ = (
        UniqueConstraint("user_uid", "book_uid", name="unique_user_book_review"),
    )

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    rating: int = Field(lt=6)  # lt => less than
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(
        sa_column=Column(
            pg.UUID,
            ForeignKey("books.uid", ondelete="CASCADE"),
            nullable=True, #CASCADE to delete reviews when the book is deleted
        )
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional[User] = Relationship(
        back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )
    book: Optional[Book] = Relationship(
        back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )
    liked_by: List[User] = Relationship(
        back_populates="liked_reviews",
        link_model=ReviewLike,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
