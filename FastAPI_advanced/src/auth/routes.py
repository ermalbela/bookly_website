from fastapi import (
    APIRouter,
    Depends,
    status,
    BackgroundTasks,
    File,
    UploadFile,
    HTTPException,
)
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
import cloudinary
import cloudinary.uploader
from .schemas import (
    UserCreateModel,
    UserProfileModel,
    UserLoginModel,
    UserBooksModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from .service import UserService
from src.db.main import get_session
from src.db.models import SavedBooks, Review, ReviewLike
from src.db.redis import add_jti_to_blocklist
from .utils import (
    create_access_token,
    verify_password,
    create_url_safe_token,
    decode_url_safe_token,
    generate_password_hash,
)
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.errors import (
    UserAlreadyExists,
    InvalidCredentials,
    InvalidToken,
    UserNotFound,
    PasswordsDontMatch,
    PasswordRequired,
)
from src.books.service import BookService
from datetime import timedelta, datetime
from src.config import Config
from src.celery_tasks import send_email

auth_router = APIRouter()
user_books_router = APIRouter()
user_service = UserService()
book_service = BookService()
role_checker = RoleChecker(["admin", "user"])

REFRESH_TOKEN_EXPIRY = 7


@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses
    subject = "Welcome to our app"
    html = "<h1>Welcome to the app</h1>"

    send_email.delay(emails, subject, html)  ##Celery Task

    return JSONResponse(content={"message": "Email sent successfully"})


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    bg_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"

    html = f"""
        <h1>Verify your email</>
        <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    emails = [email]
    subject = "Verify your email"

    send_email.delay(emails, subject, html)

    return {
        "user": new_user,
        "message": "Account created, check email to verify your account!",
    }


@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):
    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")  # return none if it doesnt exist
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={
                "message": "Account has been successfully verified",
            },
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={
            "message": "Error occured during verification",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                }
            )

            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "uid": str(user.uid),
                        "avatar_url": user.avatar_url,
                        "role": user.role,
                    },
                }
            )
    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "success": "Logged out successfully.",
            "status_code": status.HTTP_200_OK,
        }
    )


"""
1. PROVIDE THE EMAIL -> password reset request
2. SEND THE PASSWORD LINK
3. RESET PASSWORD -> password reset confirm

"""


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email

    token = create_url_safe_token({"email": email})

    link = f"http://{Config.DOMAIN}/auth/password-reset-confirm/{token}"

    html = f"""
        <h1>Reset your password</>
        <p>Please click this <a href="{link}">link</a> to reset your password</p>
    """

    emails = [email]
    subject = "Reset your password"

    send_email.delay(emails, subject, html)

    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password"
        },
        status_code=status.HTTP_200_OK,
    )


@auth_router.post("/password-reset-confirm/{token}")
async def reset_account_password(
    token: str,
    passwords: PasswordResetConfirmModel,
    session: AsyncSession = Depends(get_session),
):
    if passwords.new_password != passwords.confirm_new_password:
        raise PasswordsDontMatch()

    if not passwords.new_password:
        raise PasswordRequired()

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")  # return none if it doesnt exist
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        await user_service.update_user(
            user,
            {"password_hash": generate_password_hash(passwords.new_password)},
            session,
        )

        return JSONResponse(
            content={
                "message": "Password reset successfully",
            },
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={
            "message": "Error occured during password reset",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post("/upload/avatar")
async def upload_avatar(
    token_details: dict = Depends(AccessTokenBearer()),
    file: UploadFile = File(),
    session: AsyncSession = Depends(get_session),
):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image type"
        )

    user_email = token_details["user"]["email"]

    contents = await file.read()
    result = cloudinary.uploader.upload(contents, folder="bookly/avatars")
    avatar_url = result["secure_url"]

    user = await user_service.update_avatar_url(avatar_url, user_email, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"avatar_url": avatar_url}


@user_books_router.post("/user/{user_uid}/book/{book_uid}")
async def save_book_by_user(
    user_uid: str, book_uid: str, session: AsyncSession = Depends(get_session)
):
    await user_service.save_book(user_uid, book_uid, session)


@user_books_router.delete("/user/{user_uid}/book/{book_uid}")
async def unsave_book_by_user(
    user_uid: str, book_uid: str, session: AsyncSession = Depends(get_session)
):
    await user_service.unsave_book(user_uid, book_uid, session)


@user_books_router.get("/profile", response_model=UserProfileModel)
async def get_profile(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
) -> UserProfileModel:
    user_uid = token_details.get("user")["user_uid"]

    return await user_service.get_user_profile(user_uid, session)
