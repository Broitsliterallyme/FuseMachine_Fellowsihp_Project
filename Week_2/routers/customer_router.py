from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import customer_crud
from schemas.customer_schemas import CustomerCreate, CustomerUpdate, CustomerOut
from schemas.order_schemas import OrderOut
from schemas.payment_schemas import PaymentOut
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[CustomerOut])
def list_customers(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    logger.info(f"GET /customers skip={skip} limit={limit}")
    result = customer_crud.get_customers(db, skip=skip, limit=limit)
    logger.info(f"Returned {len(result)} customers")
    return result


@router.get("/count")
def count_customers(db: Session = Depends(get_db)):
    logger.info("GET /customers/count")
    count = customer_crud.get_customers_count(db)
    return {"table": "customers", "count": count}


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_id}")
    result = customer_crud.get_customer(db, customer_id)
    logger.info(f"Customer found: {customer_id}")
    return result


@router.get("/{customer_id}/orders", response_model=List[OrderOut])
def get_customer_orders(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_id}/orders")
    return customer_crud.get_customer_orders(db, customer_id)


@router.get("/{customer_id}/payments", response_model=List[PaymentOut])
def get_customer_payments(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"GET /customers/{customer_id}/payments")
    return customer_crud.get_customer_payments(db, customer_id)


@router.post("/", response_model=CustomerOut, status_code=201)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /customers - creating {data.customerNumber}")
    return customer_crud.create_customer(db, data)


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /customers/{customer_id}")
    return customer_crud.update_customer(db, customer_id, data)


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /customers/{customer_id}")
    return customer_crud.delete_customer(db, customer_id)
