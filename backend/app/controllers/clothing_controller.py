import base64
import os
import uuid
from fastapi import HTTPException
from backend.app.schemas.clothing_schemas import (
    UploadClothingItemRequest,
    UploadClothingItemResponse,
    TagRequest,
    TagResponse
)
from backend.app.models.clip_model import CLIPModel

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
clip_model = CLIPModel()


async def handle_upload_clothing_item(payload: UploadClothingItemRequest) -> UploadClothingItemResponse:
    # Decode base64 image and save to disk
    image_data = base64.b64decode(payload.image_base64)
    filename = payload.filename or f"{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(UPLOAD_DIR, filename)

    with open(image_path, "wb") as f:
        f.write(image_data)

    # Get tags (this could be extended with actual ML taggers later)
    embedding = clip_model.get_image_embedding(image_path)
    tags = ["style", "example"]  # Placeholder for now

    # Return mock DB response
    return UploadClothingItemResponse(
        id=str(uuid.uuid4()),
        filename=filename,
        tags=tags
    )


async def handle_tag_request(payload: TagRequest) -> TagResponse:
    # Decode image
    image_data = base64.b64decode(payload.image_base64)
    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(UPLOAD_DIR, temp_filename)

    with open(image_path, "wb") as f:
        f.write(image_data)

    # Run CLIP (This demo just returns "mock tag")
    embedding = clip_model.get_image_embedding(image_path)
    tags = ["mock", "clip", "tags"]  # Replace with actual logic

    return TagResponse(tags=tags)
