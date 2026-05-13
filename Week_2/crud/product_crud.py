from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import Product, OrderDetail
from schemas.product_schemas import ProductCreate, ProductUpdate
from logger import get_logger

logger = get_logger(__name__)


def get_productss(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching products: skip={skip}, limit={limit}")
    return db.query(Product).offset(skip).limit(limit).all()


def get_products(db: Session, id: str):
    logger.info(f"Fetching product productCode={id}")
    product = db.query(Product).filter(Product.productCode == id).first()
    if not product:
        logger.warning(f"Product not found: {id}")
        raise HTTPException(status_code=404, detail=f"Product {id} not found")
    return product


def create_products(db: Session, data: ProductCreate):
    logger.info(f"Creating product: {data.productCode}")
    try:
        product = Product(**data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        logger.info(f"Product created: {product.productCode}")
        return product
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK constraint error creating product: {e}")
        raise HTTPException(status_code=422, detail="Invalid productLine foreign key")


def update_products(db: Session, id: str, data: ProductUpdate):
    logger.info(f"Updating product: {id}")
    product = get_products(db, id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    logger.info(f"Product updated: {id}")
    return product


def delete_products(db: Session, id: str):
    logger.info(f"Deleting product: {id}")
    product = get_products(db, id)
    try:
        db.delete(product)
        db.commit()
        logger.info(f"Product deleted: {id}")
        return {"detail": "Product deleted"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Cannot delete product; it is referenced by order details")


def get_products_with_orderdetails(db: Session, id: str):
    logger.info(f"Fetching product with order details: {id}")
    product = get_products(db, id)
    return product


# --- Count ---
def get_products_count(db: Session) -> int:
    count = db.query(Product).count()
    logger.info(f"Product count: {count}")
    return count
