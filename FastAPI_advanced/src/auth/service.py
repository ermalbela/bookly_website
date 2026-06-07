from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_
from src.db.models import User, Book, SavedBooks, Review, ReviewLike, UserFollow
from .schemas import UserCreateModel
from src.reviews.schemas import ReviewDetailModel
from .utils import generate_password_hash
from src.errors import UserNotFound, BookNotFound
from fastapi import HTTPException, status
from src.books.service import BookService
from collections import defaultdict

book_service = BookService()


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

        new_user = User(**user_data_dict)

        new_user.password_hash = generate_password_hash(user_data_dict["password"])
        new_user.role = "user"

        session.add(new_user)

        await session.commit()

        return new_user

    async def update_user(self, user: User, user_data: dict, session: AsyncSession):
        for k, v in user_data.items():
            setattr(user, k, v)

        await session.commit()

        return user

    async def update_avatar_url(
        self, avatar_url: str, user_email: str, session: AsyncSession
    ):
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
            select(SavedBooks).where(
                SavedBooks.user_uid == user_uid, SavedBooks.book_uid == book_uid
            )
        )

        if existing_save.first():
            raise HTTPException(
                detail="User already saved this book!",
                status_code=status.HTTP_400_BAD_REQUEST,
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
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        await session.delete(saved_book)
        await session.commit()
    

    async def get_user_follow_details(self, user_uid: str, current_user_uid: str, session: AsyncSession):
        # check if current user follows this profile, user cant follow himself.
        is_following = False
        
        follow_result = await session.exec(
            select(UserFollow).where(
                UserFollow.follower_uid == current_user_uid,
                UserFollow.following_uid == user_uid
            )
        )
        is_following = follow_result.first() is not None

        followers_result = await session.exec(
            select(UserFollow).where(UserFollow.following_uid == user_uid)
        )
        following_result = await session.exec(
            select(UserFollow).where(UserFollow.follower_uid == user_uid)
        )

        return {
            "followers_count": len(followers_result.all()),
            "following_count": len(following_result.all()),
            "is_following": is_following
        }

    async def get_user_profile(self, user_uid: str, current_user_uid: str, session: AsyncSession):
        follow_details = await self.get_user_follow_details(user_uid, current_user_uid, session)
        user_details = await self.get_user_by_id(user_uid, session)
        user_details = {
            "first_name": user_details.first_name,
            "last_name": user_details.last_name, 
            "avatar_url": user_details.avatar_url,
            "username": user_details.username
        }
        #saved books by current user
        saved_result = await session.exec(
            select(SavedBooks).where(SavedBooks.user_uid == user_uid)
        )
        saved_book_uids = {str(s.book_uid) for s in saved_result.all()}

        all_books = await book_service.get_all_books(session)
        saved_count = defaultdict(int)
        for s in all_books:
            saved_count[str(s.uid)] += 1
            
        saved_books = [
            {
                **book.model_dump(),
                "is_saved": str(book.uid) in saved_book_uids,
                "saved_count": saved_count[str(book.uid)]
            }
            for book in all_books
            if str(book.uid) in saved_book_uids
        ]

        #reviews submitted from this user
        reviews_result = await session.exec(
            select(Review).where(Review.user_uid == user_uid)
        )
        user_reviews = reviews_result.all()

        #reviews liked by this user
        liked_result = await session.exec(
            select(ReviewLike).where(ReviewLike.user_uid == user_uid)
        )
        all_liked = liked_result.all()
        liked_uids = [str(l.review_uid) for l in all_liked]

        liked_reviews = []
        if liked_uids:
            liked_reviews_result = await session.exec(
                select(Review).where(Review.uid.in_(liked_uids))
            )
            liked_reviews = liked_reviews_result.all()

        all_review_uids = list({str(r.uid) for r in user_reviews + liked_reviews})

        likes_result = await session.exec(
            select(ReviewLike).where(ReviewLike.review_uid.in_(all_review_uids))
        ) if all_review_uids else []

        all_likes = likes_result.all() if all_review_uids else []

        likes_by_review = defaultdict(list)
        for like in all_likes:
            likes_by_review[str(like.review_uid)].append(str(like.user_uid))

        def build_review(review: Review) -> ReviewDetailModel:
            return ReviewDetailModel(
                **review.model_dump(),
                user=review.user,
                likes_count=len(likes_by_review[str(review.uid)]),
                is_liked=current_user_uid in likes_by_review[str(review.uid)]
            )

        return {
            "saved_books": saved_books,
            "reviews": [build_review(r) for r in user_reviews],
            "liked_reviews": [build_review(r) for r in liked_reviews],
            **follow_details,
            "user": {**user_details}
        }


    async def follow_user(self, follower_uid: str, following_uid: str, session: AsyncSession):
        if follower_uid == following_uid:
            raise HTTPException(
                detail="You cannot follow urself.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        existing = await session.exec(select(UserFollow).where(
            UserFollow.follower_uid == follower_uid,
            UserFollow.following_uid == following_uid
        ))
        if existing.first():
            raise HTTPException(
                detail="You already follow this user.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        follow = UserFollow(follower_uid=follower_uid, following_uid=following_uid)
        session.add(follow)
        await session.commit()
        
        
    async def unfollow_user(self, follower_uid: str, following_uid: str, session: AsyncSession):
        if follower_uid == following_uid:
            raise HTTPException(
                detail="You cannot unfollow urself.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        existing = await session.exec(select(UserFollow).where(
            UserFollow.follower_uid == follower_uid,
            UserFollow.following_uid == following_uid
        ))
        follow = existing.first()
        
        if not follow:
            raise HTTPException(
                detail="You are not currently following this user.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        await session.delete(follow)
        await session.commit()
        
        
    async def search_users(self, query: str, session: AsyncSession):
        result = await session.exec(
            select(User).where(
                or_(
                    User.username.ilike(f"%{query}%"),
                    User.first_name.ilike(f"%{query}%"),
                    User.last_name.ilike(f"%{query}%"),
                )
            ).limit(10)
        )
        return result.all()