from typing import Any, Callable
from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse

class BooklyException(Exception):
    """This is the base class for all bookly errors"""
    pass

class InvalidToken(BooklyException):
    """User has provided an invalid or expired token"""
    pass

class RevokedToken(BooklyException):
    """User has provided a token that has been revoked"""
    pass

class AccessTokenRequired(BooklyException):
    """User has provided a refresh token when an access token is needed"""
    pass

class RefreshTokenRequired(BooklyException):
    """User has provided an access token when a refresh token is needed"""
    pass

class UserAlreadyExists(BooklyException):
    """User has provided an email for an user that already exists during signup"""
    pass

class TagAlreadyExists(BooklyException):
    """Tag already exists."""
    pass

class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during signup"""
    pass

class InsufficientPermission(BooklyException):
    """User does not have the neccessary permissions to perform an action"""
    pass

class BookNotFound(BooklyException):
    """Book not found"""
    pass

class TagNotFound(BooklyException):
    """Tag not found"""
    pass

class UserNotFound(BooklyException):
    """User not found"""
    pass

class ReviewNotFound(BooklyException):
    """Review not found"""
    pass

class TagAlreadyAddedToBook(BooklyException):
    """Tag already added to book."""
    pass

class TagNotAssociatedToBook(BooklyException):
    """Tag not associated with this book"""
    pass

class AccountNotVerified(BooklyException):
    """Account not verified"""
    pass

class PasswordsDontMatch(BooklyException):
    """Passwords do not match"""
    pass

class PasswordRequired(BooklyException):
    """Password is required"""
    pass

def create_exception_handler(status_code: int, initial_detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BooklyException):
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
    return exception_handler
        
        
def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User with this email already exists",
                "error_code": "user_exists"
            }
        )
    )

    app.add_exception_handler(
        UserNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "User not found",
                "error_code": "user_not_found"
            }
        )
    )
    
    app.add_exception_handler(
        ReviewNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Review not found",
                "error_code": "review_not_found"
            }
        )
    )

    app.add_exception_handler(
        InvalidCredentials,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Invalid Email or Password",
                "error_code": "invalid_email_or_password"
            }
        )
    )

    app.add_exception_handler(
        InvalidToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or expired",
                "resolution":"Please get a new token",
                "error_code": "invalid_token"
            }
        )
    )

    app.add_exception_handler(
        RevokedToken,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            initial_detail={
                "message": "Token is invalid or has been revoked",
                "resolution":"Please get a new token",
                "error_code": "token_revoked"
            }
        )
    )

    app.add_exception_handler(
        AccessTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a valid access token",
                "error_code": "access_token_required"
            }
        )
    )


    app.add_exception_handler(
        InsufficientPermission,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "User does not have permissions to perform this action",
                "error_code": "insufficient_permission"
            }
        )
    )

    app.add_exception_handler(
        RefreshTokenRequired,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Please provide a refresh token",
                "error_code": "refresh_token_required"
            }
        )
    )

    app.add_exception_handler(
        TagAlreadyAddedToBook,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Tag has already been added to this book",
                "error_code": "tag_already_added"
            }
        )
    )

    app.add_exception_handler(
        TagAlreadyExists,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Tag with this name already exists",
                "error_code": "tag_exists"
            }
        )
    ) 

    app.add_exception_handler(
        TagNotAssociatedToBook,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Tag not associated with this book",
                "error_code": "tag_not_associated_to_book"
            }
        )
    )

    app.add_exception_handler(
        TagNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Tag Not Found",
                "error_code": "tag_not_found"
            }
        )
    )

    app.add_exception_handler(
        BookNotFound,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={
                "message": "Book Not Found",
                "error_code": "book_not_found"
            }
        )
    )
    
    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            initial_detail={
                "message": "Account not verified yet",
                "error_code": "account_not_verified",
                "resolution": "Please check your email for verification details"
            }
        )
    )
    
    app.add_exception_handler(
        PasswordsDontMatch,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Passwords do not match",
                "error_code": "passwords_not_match",
                "resolution": "Please re-write your passwords"
            }
        )
    )
    
    app.add_exception_handler(
        PasswordRequired,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            initial_detail={
                "message": "Please provide a valid password",
                "error_code": "password_required"
            }
        )
    )


    @app.exception_handler(500)
    async def internal_server_error(request, exc):
        return JSONResponse(
            content={
                "message": "Something went wrong!",
                "error_code": "server_error"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )