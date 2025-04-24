from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import base64
from io import BytesIO
from PIL import Image
from models.clip_model import CLIPModel

router = APIRouter()

# Initialize CLIPModel
clip_model = CLIPModel()

# Request and Response schemas
class TagRequest(BaseModel):
    image_base64: str  # base64 image input

class TagResponse(BaseModel):
    tags: List[str]  # list of tags

# Helper function to decode base64 to image
def decode_base64_image(image_base64: str) -> Image.Image:
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))

# API endpoint to get tags
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
