from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object ID")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# ===================
# MongoDB Schemas
# ===================

# ClothingItemModel represents what you store in MongoDB
class ClothingItemModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    filename: str
    image_path: str
    tags: List[str]
    uploaded_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ===================
# Request / Response Models
# ===================

# TagRequest / UploadClothingItemRequest are what users send in
class TagRequest(BaseModel):
    image_base64: str  # image encoded as base64 string

# TagResponse / UploadClothingItemResponse are what the API sends back
class TagResponse(BaseModel):
    tags: List[str]

class UploadClothingItemRequest(BaseModel):
    image_base64: str
    filename: Optional[str]

class UploadClothingItemResponse(BaseModel):
    id: str
    filename: str
    tags: List[str]
