from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional


class ItemSchema(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
