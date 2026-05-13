from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal


class OrderDetailCreate(BaseModel):
    orderNumber: int
    productCode: str
    quantityOrdered: int
    priceEach: Decimal
    orderLineNumber: int

    @field_validator("quantityOrdered")
    @classmethod
    def qty_positive(cls, v):
        if v <= 0:
            raise ValueError("quantityOrdered must be > 0")
        return v

    @field_validator("orderLineNumber")
    @classmethod
    def line_number_range(cls, v):
        if not (1 <= v <= 32767):
            raise ValueError("orderLineNumber must be between 1 and 32767")
        return v

    @field_validator("priceEach")
    @classmethod
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError("priceEach must be > 0")
        return v


class OrderDetailUpdate(BaseModel):
    quantityOrdered: Optional[int] = None
    priceEach: Optional[Decimal] = None
    orderLineNumber: Optional[int] = None


class OrderDetailOut(OrderDetailCreate):
    class Config:
        from_attributes = True
