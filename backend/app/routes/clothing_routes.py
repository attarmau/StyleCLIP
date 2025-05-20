import logging
from fastapi import UploadFile, File
from backend.app.controllers.clothing_detector import detect_and_crop_garments
from backend.app.controllers.tag_extractor import extract_tags_from_image  # Assume this exists
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

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/clothing", tags=["Clothing"])

@router.post("/upload", response_model=UploadClothingItemResponse)
async def upload_clothing_item(payload: UploadClothingItemRequest):
    """
    Upload a clothing item image and return the predicted garment type and feature tags.
    """
    try:
        return await handle_upload_clothing_item(payload)
    except Exception as e:
        logger.exception("Error during clothing upload")
        raise HTTPException(status_code=500, detail="Failed to process clothing upload.")

@router.post("/tag", response_model=TagResponse)
async def tag_clothing_image(payload: TagRequest):
    """
    Tag a clothing image with garment type and relevant features without storing the item.
    """
    try:
        return await handle_tag_request(payload)
    except Exception as e:
        logger.exception("Error during clothing image tagging")
        raise HTTPException(status_code=500, detail="Failed to extract tags from image.")

@router.post("/multi-tag")
async def multi_garment_tagging(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        cropped_images = detect_and_crop_garments(image_bytes)

        tags_list = []
        for garment_img in cropped_images:
            tags = extract_tags_from_image(garment_img)
            tags_list.append(tags)
        return {"garments": tags_list}
    except Exception as e:
        logger.error(f"Multi-tagging error: {e}")
        raise HTTPException(status_code=500, detail="Failed to tag garments.")
