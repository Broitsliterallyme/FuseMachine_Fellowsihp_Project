from pydantic import BaseModel, field_validator
from typing import Optional, Literal
from datetime import date


ORDER_STATUSES = Literal["Shipped", "Resolved", "Cancelled", "On Hold", "Disputed", "In Process"]


class OrderCreate(BaseModel):
    orderNumber: int
    orderDate: date
    requiredDate: date
    shippedDate: Optional[date] = None
    status: ORDER_STATUSES
    comments: Optional[str] = None
    customerNumber: int

    @field_validator("requiredDate")
    @classmethod
    def required_after_order(cls, v, info):
        if "orderDate" in info.data and v < info.data["orderDate"]:
            raise ValueError("requiredDate must be on or after orderDate")
        return v


class OrderUpdate(BaseModel):
    orderDate: Optional[date] = None
    requiredDate: Optional[date] = None
    shippedDate: Optional[date] = None
    status: Optional[ORDER_STATUSES] = None
    comments: Optional[str] = None
    customerNumber: Optional[int] = None


class OrderOut(OrderCreate):
    class Config:
        from_attributes = True
