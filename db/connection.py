from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
DATABASE_URL = "postgresql+asyncpg://postgres:1234@localhost:5433/BeefBoy"
engine = create_async_engine(url=DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(class_=AsyncSession, bind=engine)

async def get_db():
    async  with AsyncSessionLocal() as session:
        yield session


