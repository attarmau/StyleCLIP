# /backend/app/config/settings.py

import os

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Default to local MongoDB
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "clothing_db")
    API_KEY: str = os.getenv("API_KEY", "your-api-key")  # Example for API keys

settings = Settings()
