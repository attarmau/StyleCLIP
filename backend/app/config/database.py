from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings

client = None
db = None

async def init_db():
    global client, db
    client = AsyncIOMotorClient(settings.MONGO_URI) 
    db = client[settings.MONGO_DB_NAME]  # Name of the database
    print("Database connected")

async def close_db():
    global client
    client.close()
    print("Database connection closed")
