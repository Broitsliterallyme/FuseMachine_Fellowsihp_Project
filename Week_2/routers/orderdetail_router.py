from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import orderdetail_crud
from schemas.orderdetail_schemas import OrderDetailCreate, OrderDetailUpdate, OrderDetailOut
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[OrderDetailOut])
def list_orderdetails(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    logger.info(f"GET /orderdetails skip={skip} limit={limit}")
    return orderdetail_crud.get_orderdetailss(db, skip=skip, limit=limit)


@router.get("/count")
def count_orderdetails(db: Session = Depends(get_db)):
    logger.info("GET /orderdetails/count")
    return {"table": "orderdetails", "count": orderdetail_crud.get_orderdetails_count(db)}


@router.get("/order/{orderNumber}", response_model=List[OrderDetailOut])
def get_details_by_order(orderNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /orderdetails/order/{orderNumber}")
    return orderdetail_crud.get_orderdetails_by_order(db, orderNumber)


@router.get("/product/{productCode}", response_model=List[OrderDetailOut])
def get_details_by_product(productCode: str, db: Session = Depends(get_db)):
    logger.info(f"GET /orderdetails/product/{productCode}")
    return orderdetail_crud.get_orderdetails_by_product(db, productCode)


@router.get("/{orderNumber}/{productCode}", response_model=OrderDetailOut)
def get_orderdetail(orderNumber: int, productCode: str, db: Session = Depends(get_db)):
    logger.info(f"GET /orderdetails/{orderNumber}/{productCode}")
    return orderdetail_crud.get_orderdetails(db, orderNumber, productCode)


@router.post("/", response_model=OrderDetailOut, status_code=201)
def create_orderdetail(data: OrderDetailCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /orderdetails - {data.orderNumber}/{data.productCode}")
    return orderdetail_crud.create_orderdetails(db, data)


@router.put("/{orderNumber}/{productCode}", response_model=OrderDetailOut)
def update_orderdetail(orderNumber: int, productCode: str, data: OrderDetailUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /orderdetails/{orderNumber}/{productCode}")
    return orderdetail_crud.update_orderdetails(db, orderNumber, productCode, data)


@router.delete("/{orderNumber}/{productCode}")
def delete_orderdetail(orderNumber: int, productCode: str, db: Session = Depends(get_db)):
    logger.info(f"DELETE /orderdetails/{orderNumber}/{productCode}")
    return orderdetail_crud.delete_orderdetails(db, orderNumber, productCode)
