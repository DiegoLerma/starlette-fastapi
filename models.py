from typing import Optional
from pydantic import BaseModel


class ItemModel(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
