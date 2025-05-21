from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import base64
from io import BytesIO
from PIL import Image, UnidentifiedImageError
from backend.app.models.clip_model import CLIPModel
from backend.app.aws.rekognition_wrapper import detect_garments
from backend.app.utils.image_utils import crop_by_bounding_box
from .tag_extractor import get_tags_from_clip

router = APIRouter()

clip_model = CLIPModel()

class TagRequest(BaseModel):
    image_base64: str 

class TagResponse(BaseModel):
    tags: List[str]  # list of tags

def decode_base64_image(image_base64: str) -> Image.Image:
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))

@router.post("/tag", response_model=TagResponse)
def tag_image(request: TagRequest):
    try:
        # Decode the base64 image
        image = decode_base64_image(request.image_base64)
        
        # Here you can use your model's methods to get tags
        # For instance, you could find the most similar images or tags here
        tags = ["example_tag_1", "example_tag_2"]  # Replace with actual logic from CLIPModel
        
        return TagResponse(tags=tags)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def tag_image_with_aws_and_clip(image_bytes: bytes) -> List[dict]:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError:
        raise ValueError("Invalid image format")

    try:
        garment_boxes = detect_garments(image_bytes)
    except Exception as e:
        raise RuntimeError(f"AWS Rekognition failed: {str(e)}")

    results = []
    for box in garment_boxes:
        try:
            cropped = crop_by_bounding_box(image, box)
            tags = get_tags_from_clip(cropped)
            results.append({
                "box": box,
                "tags": tags,
            })
        except Exception as e:
            results.append({
                "box": box,
                "tags": [],
                "error": str(e),
            })
    return results
