from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from typing import List, Dict, Optional
from datetime import datetime
from bson import ObjectId

# --------------------------
# Custom ObjectId for Pydantic v2
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
    def __get_pydantic_json_schema__(
        cls, core_schema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema


# --------------------------
# MongoDB Document Schema
# --------------------------
class GarmentTags(BaseModel):
    garment_type: str
    aws_label: Optional[str] = None
    box: Optional[Dict[str, float]] = None  # BoundingBox coordinates
    tags: Dict[str, List[str]]  # e.g., {"color": ["red","blue"], "fit":["slim","relaxed"]}


class ClothingItemInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    filename: str
    image_path: str
    garments: List[GarmentTags]
    uploaded_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
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
class GarmentResponse(BaseModel):
    garment_type: str
    aws_label: Optional[str] = None
    box: Optional[Dict[str, float]] = None
    tags: Dict[str, List[str]]  # per-category top N tags


class UploadClothingItemResponse(BaseModel):
    id: str
    filename: str
    garments: List[GarmentResponse]


class TagResponse(BaseModel):
    garments: List[GarmentResponse]
