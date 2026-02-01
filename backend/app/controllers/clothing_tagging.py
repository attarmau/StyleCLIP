from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Optional
from PIL import Image, UnidentifiedImageError
import io
from backend.app.aws.rekognition_wrapper import rekognition
from backend.app.utils.image_utils import crop_by_bounding_box
from backend.app.controllers.tag_extractor import get_tags_from_clip

router = APIRouter()

class GarmentTag(BaseModel):
    aws_label: Optional[str]
    box: Optional[Dict[str, float]]
    garment_type: str
    tags: Dict[str, List[str]]

class TagResponse(BaseModel):
    image_name: Optional[str]
    results: List[GarmentTag]

# Core Tagging Logic
def tag_image_per_garment(image_bytes: bytes, image_name: str, min_confidence: int = 50):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid image format")

    try:
        response = rekognition.detect_labels(
            Image={"Bytes": image_bytes}, MinConfidence=min_confidence
        )
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
                "tags": {k: v[:3] for k, v in tags_result.get("tags", {}).items()},
            })

    # fallback if Rekognition detects nothing
    if not results:
        tags_result = get_tags_from_clip(image)
        results.append({
            "aws_label": None,
            "box": None,
            "garment_type": tags_result.get("garment_type", "Unknown"),
            "tags": {k: v[:3] for k, v in tags_result.get("tags", {}).items()},
        })

    return results

@router.post("/tag", response_model=TagResponse)
async def tag_image_endpoint(file: UploadFile = File(...)):
    """
    Endpoint: /api/v1/clothing/tag
    Description: Upload an image to get per-garment tags and attributes.
    """
    try:
        image_bytes = await file.read()
        image_name = file.filename
        results = tag_image_per_garment(image_bytes, image_name)
        return TagResponse(image_name=image_name, results=results)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
