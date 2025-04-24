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
from backend.app.config.tag_list_en import GARMENT_TYPES

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
clip_model = CLIPModel()  # Initialize the CLIP model

def determine_garment_type(embedding):
    garment_types = list(GARMENT_TYPES.keys())
    similarities = {
        gt: clip_model.get_similarity(embedding, gt) for gt in garment_types
    }
    return max(similarities, key=similarities.get)

def extract_features(embedding, garment_type):
    if garment_type not in GARMENT_TYPES:
        return {"error": "Unknown garment type"}

    def best_match(options):
        similarities = {
            label: clip_model.get_similarity(embedding, label) for label in options
        }
        return max(similarities, key=similarities.get)

    tags_config = GARMENT_TYPES[garment_type]
    return {
        feature: best_match(options) for feature, options in tags_config.items()
    }

async def handle_upload_clothing_item(payload: UploadClothingItemRequest) -> UploadClothingItemResponse:
    image_data = base64.b64decode(payload.image_base64)
    filename = payload.filename or f"{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(UPLOAD_DIR, filename)

    with open(image_path, "wb") as f:
        f.write(image_data)

    try:
        embedding = clip_model.get_image_embedding(image_path)
        garment_type = determine_garment_type(embedding)
        feature_tags = extract_features(embedding, garment_type)
        tags = {"garment_type": garment_type, **feature_tags}
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
        garment_type = determine_garment_type(embedding)
        feature_tags = extract_features(embedding, garment_type)
        tags = [garment_type] + list(feature_tags.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    return TagResponse(tags=tags)
