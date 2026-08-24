from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Annotated

DATABASE_URL = "sqlite+aiosqlite:///./trendflow_gym.db"

engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

timestamp = Annotated[datetime, mapped_column(default=datetime.now)]

class StudentModel(Base):
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    document: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    financial_due_date: Mapped[datetime]
    last_evaluation: Mapped[datetime | None]

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)