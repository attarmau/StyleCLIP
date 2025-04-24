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
clip_model = CLIPModel()  # Initialize the CLIP model

async def handle_upload_clothing_item(payload: UploadClothingItemRequest) -> UploadClothingItemResponse:
    # Decode base64 image and save to disk
    image_data = base64.b64decode(payload.image_base64)
    filename = payload.filename or f"{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(UPLOAD_DIR, filename)

    with open(image_path, "wb") as f:
        f.write(image_data)

    # Get image embedding using the CLIP model
    try:
        embedding = clip_model.get_image_embedding(image_path)
        # Placeholder tags based on the image (you can use real logic here)
        tags = ["style", "example"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    # Return response with mock data (in actual, this could involve storing data in DB)
    return UploadClothingItemResponse(
        id=str(uuid.uuid4()),
        filename=filename,
        tags=tags
    )


async def handle_tag_request(payload: TagRequest) -> TagResponse:
    # Decode base64 image and save as temporary file
    image_data = base64.b64decode(payload.image_base64)
    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(UPLOAD_DIR, temp_filename)

    with open(image_path, "wb") as f:
        f.write(image_data)

    # Run the CLIP model to get the embedding and tags
    try:
        embedding = clip_model.get_image_embedding(image_path)
        # Placeholder for actual tag logic (replace with real logic using embedding)
        tags = ["mock", "clip", "tags"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    return TagResponse(tags=tags)
