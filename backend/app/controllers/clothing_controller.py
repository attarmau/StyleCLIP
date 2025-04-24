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
from backend.app.controllers.tag_extractor import TagExtractor
from backend.app.config.tag_list_en import GARMENT_TYPES  # GARMENT_TYPES contains full tag hierarchy

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize model and tag extractor once
clip_model = CLIPModel()
tag_extractor = TagExtractor(tag_dict=GARMENT_TYPES)

async def handle_upload_clothing_item(payload: UploadClothingItemRequest) -> UploadClothingItemResponse:
    # Decode base64 image and save to disk
    image_data = base64.b64decode(payload.image_base64)
    filename = payload.filename or f"{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(UPLOAD_DIR, filename)

    with open(image_path, "wb") as f:
        f.write(image_data)

    try:
        # Step 1: Get embedding
        embedding = clip_model.get_image_embedding(image_path)

        # Step 2: Garment Type Classification
        garment_type = tag_extractor.determine_garment_type(embedding)

        # Step 3: Feature Tag Extraction (based on that garment type)
        if garment_type != "Unknown":
            tags = tag_extractor.extract_tags(embedding, garment_type)
        else:
            tags = {"error": "Unknown garment type"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    return UploadClothingItemResponse(
        id=str(uuid.uuid4()),
        filename=filename,
        tags=tags
    )

async def handle_tag_request(payload: TagRequest) -> TagResponse:
    image_data = base64.b64decode(payload.image_base64)
    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(UPLOAD_DIR, temp_filename)

    with open(image_path, "wb") as f:
        f.write(image_data)

    try:
        embedding = clip_model.get_image_embedding(image_path)
        garment_type = tag_extractor.determine_garment_type(embedding)
        if garment_type != "Unknown":
            tags = tag_extractor.extract_tags(embedding, garment_type)
        else:
            tags = {"error": "Unknown garment type"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    return TagResponse(tags=tags)
