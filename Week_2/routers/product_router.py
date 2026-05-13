from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import product_crud
from schemas.product_schemas import ProductCreate, ProductUpdate, ProductOut
from schemas.orderdetail_schemas import OrderDetailOut
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[ProductOut])
def list_products(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    logger.info(f"GET /products skip={skip} limit={limit}")
    return product_crud.get_productss(db, skip=skip, limit=limit)


@router.get("/count")
def count_products(db: Session = Depends(get_db)):
    logger.info("GET /products/count")
    return {"table": "products", "count": product_crud.get_products_count(db)}


@router.get("/{productCode}", response_model=ProductOut)
def get_product(productCode: str, db: Session = Depends(get_db)):
    logger.info(f"GET /products/{productCode}")
    return product_crud.get_products(db, productCode)


@router.get("/{productCode}/orderdetails", response_model=List[OrderDetailOut])
def get_product_orderdetails(productCode: str, db: Session = Depends(get_db)):
    logger.info(f"GET /products/{productCode}/orderdetails")
    product = product_crud.get_products_with_orderdetails(db, productCode)
    return product.order_details or []


@router.post("/", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /products - {data.productCode}")
    return product_crud.create_products(db, data)


@router.put("/{productCode}", response_model=ProductOut)
def update_product(productCode: str, data: ProductUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /products/{productCode}")
    return product_crud.update_products(db, productCode, data)


@router.delete("/{productCode}")
def delete_product(productCode: str, db: Session = Depends(get_db)):
    logger.info(f"DELETE /products/{productCode}")
    return product_crud.delete_products(db, productCode)
