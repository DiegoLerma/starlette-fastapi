from pydantic import BaseModel, Field
from typing import Optional

class ItemModel(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
