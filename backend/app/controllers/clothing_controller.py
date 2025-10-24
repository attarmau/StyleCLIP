import base64
import os
import uuid
from io import BytesIO
from PIL import Image
from fastapi import HTTPException
from backend.app.controllers.clothing_tagging import crop_by_bounding_box
from backend.app.controllers.tag_extractor import get_tags_from_clip
from backend.app.aws.rekognition_wrapper import rekognition
from backend.app.schemas.clothing_schemas import (
    UploadClothingItemRequest,
    UploadClothingItemResponse,
    TagRequest,
    TagResponse
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MIN_CONFIDENCE = 50  # minimum detection threshold for Rekognition

def tag_image_per_garment(image_path: str, min_confidence=MIN_CONFIDENCE):
    """
    Detect garments with AWS Rekognition, crop by bounding box, tag each with CLIP,
    and avoid duplicate garment types in the result.
    """
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image = Image.open(image_path).convert("RGB")

    results = []
    seen_garment_types = set()

    try:
        response = rekognition.detect_labels(Image={'Bytes': image_bytes}, MinConfidence=min_confidence)
    except Exception as e:
        print(f"AWS Rekognition error: {e}")
        response = {"Labels": []}

    for label in response.get("Labels", []):
        for instance in label.get("Instances", []):
            box = instance.get("BoundingBox")
            if not box:
                continue

            cropped = crop_by_bounding_box(image, box)
            tags_result = get_tags_from_clip(cropped)
            g_type = tags_result.get("garment_type", "Unknown")

            # Avoid repeating identical garment types
            if g_type in seen_garment_types:
                continue
            seen_garment_types.add(g_type)

            results.append({
                "aws_label": label.get("Name", "Unknown"),
                "box": box,
                "garment_type": g_type,
                "tags": {k: v[:3] for k, v in tags_result.get("tags", {}).items()}
            })

    # Fallback: if Rekognition detects nothing
    if not results:
        tags_result = get_tags_from_clip(image)
        results.append({
            "aws_label": None,
            "box": None,
            "garment_type": tags_result.get("garment_type", "Unknown"),
            "tags": {k: v[:3] for k, v in tags_result.get("tags", {}).items()}
        })

    return results

async def handle_upload_clothing_item(payload: UploadClothingItemRequest) -> UploadClothingItemResponse:
    """
    Handles upload for clothing tagging. Returns structured JSON with garment types and tags.
    """
    try:
        image_data = base64.b64decode(payload.image_base64)
        filename = payload.filename or f"{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(UPLOAD_DIR, filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        # Run Rekognition + CLIP tagging
        results = tag_image_per_garment(image_path)

        return UploadClothingItemResponse(
            id=str(uuid.uuid4()),
            filename=filename,
            tags=results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")



async def handle_tag_request(payload: TagRequest) -> TagResponse:
    """
    Handles single-image tagging requests (no need to store permanently).
    """
    try:
        image_data = base64.b64decode(payload.image_base64)
        temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
        image_path = os.path.join(UPLOAD_DIR, temp_filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        results = tag_image_per_garment(image_path)

        return TagResponse(tags=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
