from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal
from datetime import date


class PaymentCreate(BaseModel):
    customerNumber: int
    checkNumber: str
    paymentDate: date
    amount: Decimal

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be > 0")
        return v

    @field_validator("paymentDate")
    @classmethod
    def not_future(cls, v):
        if v > date.today():
            raise ValueError("paymentDate cannot be in the future")
        return v


class PaymentUpdate(BaseModel):
    paymentDate: Optional[date] = None
    amount: Optional[Decimal] = None


class PaymentOut(PaymentCreate):
    class Config:
        from_attributes = True
