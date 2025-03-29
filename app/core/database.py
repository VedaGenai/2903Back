from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Replace with your actual database connection string
DATABASE_URL = "postgresql+asyncpg://postgres:Temp1234@localhost/fasthire99"

# Create async engine
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,  # Set to False in production
    future=True
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class for declarative models
Base = declarative_base()

# Dependency to get database session
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session