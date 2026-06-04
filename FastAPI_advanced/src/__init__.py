from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import book_router
from contextlib import asynccontextmanager
import cloudinary
from src.db.main import init_db
from src.auth.routes import auth_router
from src.reviews.routes import review_router, user_review_router
from src.tags.routes import tag_router, book_tag_router
from .errors import register_all_errors
from .middleware import register_middleware
from .config import Config

# @asynccontextmanager
# async def life_span(app: FastAPI): ##Do something when app is starting and when it stops
#     print(f"server is starting ...")
#     await init_db()
#     yield
#     print(f"server has been stopped")

version = "v1"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version,
    contact={
        "name": "Ermal",
        "email": "ermal.bela1@gmail.com"
    },
    redoc_url="/redoc"
    # lifespan=life_span ###Used for starting db only, removed after modifying tables###
)

cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET,
)

register_all_errors(app)
register_middleware(app)


app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/review", tags=['reviews'])
app.include_router(tag_router, prefix=f"/api/{version}/tag", tags=['tags'])
app.include_router(book_tag_router, prefix=f"/api/{version}/book_tag", tags=['book_tags'])
app.include_router(user_review_router, prefix=f"/api/{version}/user_review", tags=['user_reviews'])