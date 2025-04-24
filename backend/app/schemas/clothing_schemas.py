from pydantic import BaseModel, Field, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from typing import List, Optional
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
class ClothingItemInDB(BaseModel):  # formerly ClothingItemModel
    id: Optional[PyObjectId] = Field(alias="_id")
    filename: str
    image_path: str
    tags: List[str]
    uploaded_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True  # replaces `allow_population_by_field_name` in v2
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
