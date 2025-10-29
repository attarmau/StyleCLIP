import base64
import os
import uuid
from fastapi import HTTPException
from PIL import Image
from backend.app.controllers.clothing_tagging import crop_by_bounding_box
from backend.app.controllers.tag_extractor import get_tags_from_clip
from backend.app.aws.rekognition_wrapper import rekognition
from backend.app.schemas.clothing_schemas import (
    UploadClothingItemRequest,
    UploadClothingItemResponse,
)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MIN_CONFIDENCE = 50

async def handle_upload_clothing_item(payload: UploadClothingItemRequest) -> UploadClothingItemResponse:
    image_data = base64.b64decode(payload.image_base64)
    filename = payload.filename or f"{uuid.uuid4().hex}.jpg"
    image_path = os.path.join(UPLOAD_DIR, filename)
    with open(image_path, "wb") as f:
        f.write(image_data)

    image = Image.open(image_path).convert("RGB")

    try:
        # Run AWS Rekognition
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = rekognition.detect_labels(Image={'Bytes': image_bytes}, MinConfidence=MIN_CONFIDENCE)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AWS Rekognition error: {str(e)}")

    results = []
    seen_garment_types = set()

    for label in response.get("Labels", []):
        for instance in label.get("Instances", []):
            box = instance.get("BoundingBox")
            if not box:
                continue

            cropped = crop_by_bounding_box(image, box)
            tags_result = get_tags_from_clip(cropped)
            g_type = tags_result.get("garment_type", "Unknown")

            if g_type in seen_garment_types:
                continue
            seen_garment_types.add(g_type)

            results.append({
                "aws_label": label.get("Name", "Unknown"),
                "box": box,
                "garment_type": g_type,
                "tags": {k: v[:10] for k, v in tags_result.get("tags", {}).items()}
            })

    # Fallback if no Rekognition garments found
    if not results:
        tags_result = get_tags_from_clip(image)
        results.append({
            "aws_label": None,
            "box": None,
            "garment_type": tags_result.get("garment_type", "Unknown"),
            "tags": {k: v[:10] for k, v in tags_result.get("tags", {}).items()}
        })

    # Return as structured response
    return UploadClothingItemResponse(
        id=str(uuid.uuid4()),
        filename=filename,
        tags={"garments": results}  # key "garments" = multiple garment results
    )
