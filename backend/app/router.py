from fastapi import APIRouter, HTTPException
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from models import TagRequest, TagResponse, UploadClothingItemRequest, UploadClothingItemResponse, ClothingItemModel
from tag_extractor import extract_tags_from_base64
from bson import ObjectId

import base64
import os
import uuid

router = APIRouter()

# MongoDB client setup
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
clothing_collection = db["clothing_items"]


@router.post("/tag", response_model=TagResponse)
async def tag_image(data: TagRequest):
    try:
        tags = extract_tags_from_base64(data.image_base64)
        return {"tags": tags}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tagging failed: {e}")


@router.post("/upload", response_model=UploadClothingItemResponse)
async def upload_item(data: UploadClothingItemRequest):
    try:
        # Decode and save image
        image_data = base64.b64decode(data.image_base64)
        filename = data.filename or f"{uuid.uuid4()}.jpg"
        image_path = os.path.join("images", filename)
        os.makedirs("images", exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(image_data)

        # Extract tags
        tags = extract_tags_from_base64(data.image_base64)

        # Store in MongoDB
        new_item = {
            "filename": filename,
            "image_path": image_path,
            "tags": tags,
        }
        result = await clothing_collection.insert_one(new_item)

        return {
            "id": str(result.inserted_id),
            "filename": filename,
            "tags": tags,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {e}")


@router.get("/items", response_model=list[ClothingItemModel])
async def get_all_items():
    items = []
    async for item in clothing_collection.find():
        item["_id"] = str(item["_id"])
        items.append(item)
    return items
