from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId


# --------------------------
# Custom ObjectId for Pydantic
# --------------------------
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


# --------------------------
# MongoDB Document Schema
# --------------------------
class ClothingItemInDB(BaseModel):  # formerly ClothingItemModel
    id: Optional[PyObjectId] = Field(alias="_id")
    filename: str
    image_path: str
    tags: List[str]
    uploaded_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# --------------------------
# API Request Schemas
# --------------------------
class UploadClothingItemRequest(BaseModel):
    image_base64: str
    filename: Optional[str]


class TagRequest(BaseModel):
    image_base64: str  # image encoded as base64 string


# --------------------------
# API Response Schemas
# --------------------------
class UploadClothingItemResponse(BaseModel):
    id: str
    filename: str
    tags: List[str]


class TagResponse(BaseModel):
    tags: List[str]
