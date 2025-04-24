from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from backend.app.config.settings import settings
from typing import AsyncGenerator

client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None

async def init_db():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    print("Database connected")

async def close_db():
    global client
    client.close()
    print("Database connection closed")

async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    yield db
