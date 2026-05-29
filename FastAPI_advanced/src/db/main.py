from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Config


engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    # echo=True ## Echo=True to show the logs of db
))

async def init_db() -> None:
    async with engine.begin() as conn:
        from src.db.models import Book
        
        await conn.run_sync(SQLModel.metadata.create_all)
        
        
async def get_session() -> AsyncSession:
    
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with Session() as session:
        #session is created, opened
        
        yield session #session is handed to the route
        
        #session is closed automatically