from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import payment_crud
from schemas.payment_schemas import PaymentCreate, PaymentUpdate, PaymentOut
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[PaymentOut])
def list_payments(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    logger.info(f"GET /payments skip={skip} limit={limit}")
    return payment_crud.get_paymentss(db, skip=skip, limit=limit)


@router.get("/count")
def count_payments(db: Session = Depends(get_db)):
    logger.info("GET /payments/count")
    return {"table": "payments", "count": payment_crud.get_payments_count(db)}


@router.get("/customer/{customerNumber}", response_model=List[PaymentOut])
def get_payments_by_customer(customerNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /payments/customer/{customerNumber}")
    return payment_crud.get_payments_by_customer(db, customerNumber)


@router.get("/{customerNumber}/{checkNumber}", response_model=PaymentOut)
def get_payment(customerNumber: int, checkNumber: str, db: Session = Depends(get_db)):
    logger.info(f"GET /payments/{customerNumber}/{checkNumber}")
    return payment_crud.get_payments(db, customerNumber, checkNumber)


@router.post("/", response_model=PaymentOut, status_code=201)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /payments - {data.customerNumber}/{data.checkNumber}")
    return payment_crud.create_payments(db, data)


@router.put("/{customerNumber}/{checkNumber}", response_model=PaymentOut)
def update_payment(customerNumber: int, checkNumber: str, data: PaymentUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /payments/{customerNumber}/{checkNumber}")
    return payment_crud.update_payments(db, customerNumber, checkNumber, data)


@router.delete("/{customerNumber}/{checkNumber}")
def delete_payment(customerNumber: int, checkNumber: str, db: Session = Depends(get_db)):
    logger.info(f"DELETE /payments/{customerNumber}/{checkNumber}")
    return payment_crud.delete_payments(db, customerNumber, checkNumber)
