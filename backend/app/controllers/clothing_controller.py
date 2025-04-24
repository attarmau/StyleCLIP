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
from backend.app.config.tag_list_en import GARMENT_TYPES  # Import the tag categories

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

        # Use the embedding to determine the garment type
        # This is where you'd implement your actual garment detection logic
        garment_type = "Tops"  # Example output, adjust based on model output

        if garment_type in GARMENT_TYPES:
            garment_tags = GARMENT_TYPES[garment_type]  # Retrieve tags for the garment type
            # In a real system, you'd extract actual garment-specific tags based on the model output
            tags = garment_tags  # For now, just returning all tags for the "Tops" category
        else:
            tags = []

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    # Return response with mock data (in actual, this could involve storing data in DB)
    return UploadClothingItemResponse(
        id=str(uuid.uuid4()),
        filename=filename,
        tags=tags
    )

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

        # Use the embedding to determine the garment type (this will be handled by the classification logic)
        garment_type = determine_garment_type(embedding)  # This would be your custom classification step

        if garment_type in GARMENT_TYPES:
            garment_tags = GARMENT_TYPES[garment_type]  # Retrieve tags for the identified garment type
            tags = garment_tags
        else:
            tags = ["Unknown garment type"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

    return UploadClothingItemResponse(
        id=str(uuid.uuid4()),
        filename=filename,
        tags=tags
    )
