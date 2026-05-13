from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import order_crud
from schemas.order_schemas import OrderCreate, OrderUpdate, OrderOut
from schemas.orderdetail_schemas import OrderDetailOut
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[OrderOut])
def list_orders(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    logger.info(f"GET /orders skip={skip} limit={limit}")
    return order_crud.get_orderss(db, skip=skip, limit=limit)


@router.get("/count")
def count_orders(db: Session = Depends(get_db)):
    logger.info("GET /orders/count")
    return {"table": "orders", "count": order_crud.get_orders_count(db)}


@router.get("/customer/{customerNumber}", response_model=List[OrderOut])
def get_orders_by_customer(customerNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /orders/customer/{customerNumber}")
    return order_crud.get_orders_by_customer(db, customerNumber)


@router.get("/{orderNumber}", response_model=OrderOut)
def get_order(orderNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /orders/{orderNumber}")
    return order_crud.get_orders(db, orderNumber)


@router.get("/{orderNumber}/orderdetails", response_model=List[OrderDetailOut])
def get_order_details(orderNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /orders/{orderNumber}/orderdetails")
    order = order_crud.get_orders_with_orderdetails(db, orderNumber)
    return order.order_details or []


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /orders - {data.orderNumber}")
    return order_crud.create_orders(db, data)


@router.put("/{orderNumber}", response_model=OrderOut)
def update_order(orderNumber: int, data: OrderUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /orders/{orderNumber}")
    return order_crud.update_orders(db, orderNumber, data)


@router.delete("/{orderNumber}")
def delete_order(orderNumber: int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /orders/{orderNumber}")
    return order_crud.delete_orders(db, orderNumber)
