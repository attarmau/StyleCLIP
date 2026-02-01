import base64
import os
import uuid
from fastapi import HTTPException
from PIL import Image

from backend.app.pipeline.inference_pipeline import InferencePipeline
from backend.app.schemas.clothing_schemas import (
    UploadClothingItemRequest,
    UploadClothingItemResponse,
    TagRequest,
    TagResponse
)

# Upload directory for temporary storage
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Minimum confidence for AWS Rekognition detection
MIN_CONFIDENCE = 50


async def handle_upload_clothing_item(payload: UploadClothingItemRequest) -> UploadClothingItemResponse:
    """
    Endpoint logic for handling clothing image upload and multi-garment tagging.
    Uses AWS Rekognition for detection, and CLIP for tag extraction per garment.
    """
    # Step 1: Decode image
    try:
        image_data = base64.b64decode(payload.image_base64)
        filename = payload.filename or f"{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(UPLOAD_DIR, filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        image = Image.open(image_path).convert("RGB")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

    # Step 2: Run Automated Inference Pipeline
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        pipeline = InferencePipeline(min_confidence=MIN_CONFIDENCE)
        results = pipeline.process_image(image, image_bytes)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference Pipeline error: {str(e)}")

    # Step 3: Return structured response
    return UploadClothingItemResponse(
        id=str(uuid.uuid4()),
        filename=filename,
        tags={"garments": results}
    )


async def handle_tag_request(payload: TagRequest) -> TagResponse:
    """
    Optional: a simpler endpoint to return tags from a single image
    (without Rekognition detection).
    """
    try:
        image_data = base64.b64decode(payload.image_base64)
        temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(UPLOAD_DIR, temp_filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        image = Image.open(image_path).convert("RGB")
        tags_result = get_tags_from_clip(image)

        return TagResponse(tags=tags_result.get("tags", {}))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
