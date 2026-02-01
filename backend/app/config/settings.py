import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # MongoDB configuration
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017") 
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "clothing_db")

    API_KEY: str = os.getenv("API_KEY", "your-api-key-here")

    # Application settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "mysecretkey")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"  
    PORT: int = int(os.getenv("PORT", 8000))  # Default port to 8000

settings = Settings()
