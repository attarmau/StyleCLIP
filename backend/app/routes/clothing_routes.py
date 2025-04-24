import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter, HTTPException
from backend.app.schemas.clothing_schemas import (
    UploadClothingItemRequest,
    UploadClothingItemResponse,
    TagRequest,
    TagResponse
)
from backend.app.controllers.clothing_controller import (
    handle_upload_clothing_item,
    handle_tag_request
)

router = APIRouter(prefix="/clothing", tags=["Clothing"])

# Endpoint to upload clothing item and return tags
@router.post("/upload", response_model=UploadClothingItemResponse)
async def upload_clothing_item(payload: UploadClothingItemRequest):
    try:
        return await handle_upload_clothing_item(payload)
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process clothing upload.")

@router.post("/tag", response_model=TagResponse)
async def tag_clothing_image(payload: TagRequest):
    try:
        return await handle_tag_request(payload)
    except Exception as e:
        logger.error(f"Tagging error: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract tags from image.")
