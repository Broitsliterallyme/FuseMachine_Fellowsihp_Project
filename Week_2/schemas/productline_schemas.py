from pydantic import BaseModel
from typing import Optional


class ProductLineCreate(BaseModel):
    productLine: str
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None
    # image excluded from API (binary data)


class ProductLineUpdate(BaseModel):
    textDescription: Optional[str] = None
    htmlDescription: Optional[str] = None


class ProductLineOut(ProductLineCreate):
    class Config:
        from_attributes = True
