from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import productline_crud
from schemas.productline_schemas import ProductLineCreate, ProductLineUpdate, ProductLineOut
from schemas.product_schemas import ProductOut
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[ProductLineOut])
def list_productlines(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    logger.info(f"GET /productlines skip={skip} limit={limit}")
    return productline_crud.get_productliness(db, skip=skip, limit=limit)


@router.get("/count")
def count_productlines(db: Session = Depends(get_db)):
    logger.info("GET /productlines/count")
    return {"table": "productlines", "count": productline_crud.get_productlines_count(db)}


@router.get("/{productLine}", response_model=ProductLineOut)
def get_productline(productLine: str, db: Session = Depends(get_db)):
    logger.info(f"GET /productlines/{productLine}")
    return productline_crud.get_productlines(db, productLine)


@router.get("/{productLine}/products", response_model=List[ProductOut])
def get_productline_products(productLine: str, db: Session = Depends(get_db)):
    logger.info(f"GET /productlines/{productLine}/products")
    pl = productline_crud.get_productlines_with_products(db, productLine)
    return pl.products or []


@router.post("/", response_model=ProductLineOut, status_code=201)
def create_productline(data: ProductLineCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /productlines - {data.productLine}")
    return productline_crud.create_productlines(db, data)


@router.put("/{productLine}", response_model=ProductLineOut)
def update_productline(productLine: str, data: ProductLineUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /productlines/{productLine}")
    return productline_crud.update_productlines(db, productLine, data)


@router.delete("/{productLine}")
def delete_productline(productLine: str, db: Session = Depends(get_db)):
    logger.info(f"DELETE /productlines/{productLine}")
    return productline_crud.delete_productlines(db, productLine)
