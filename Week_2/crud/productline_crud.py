from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import ProductLine
from schemas.productline_schemas import ProductLineCreate, ProductLineUpdate
from logger import get_logger

logger = get_logger(__name__)


def get_productliness(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching product lines: skip={skip}, limit={limit}")
    return db.query(ProductLine).offset(skip).limit(limit).all()


def get_productlines(db: Session, id: str):
    logger.info(f"Fetching product line: {id}")
    pl = db.query(ProductLine).filter(ProductLine.productLine == id).first()
    if not pl:
        logger.warning(f"ProductLine not found: {id}")
        raise HTTPException(status_code=404, detail=f"ProductLine '{id}' not found")
    return pl


def create_productlines(db: Session, data: ProductLineCreate):
    logger.info(f"Creating product line: {data.productLine}")
    pl = ProductLine(**data.model_dump())
    db.add(pl)
    db.commit()
    db.refresh(pl)
    logger.info(f"ProductLine created: {pl.productLine}")
    return pl


def update_productlines(db: Session, id: str, data: ProductLineUpdate):
    logger.info(f"Updating product line: {id}")
    pl = get_productlines(db, id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pl, field, value)
    db.commit()
    db.refresh(pl)
    logger.info(f"ProductLine updated: {id}")
    return pl


def delete_productlines(db: Session, id: str):
    logger.info(f"Deleting product line: {id}")
    pl = get_productlines(db, id)
    try:
        db.delete(pl)
        db.commit()
        logger.info(f"ProductLine deleted: {id}")
        return {"detail": "ProductLine deleted"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Cannot delete; products still reference this product line")


def get_productlines_with_products(db: Session, id: str):
    logger.info(f"Fetching product line with products: {id}")
    return get_productlines(db, id)


# --- Count ---
def get_productlines_count(db: Session) -> int:
    count = db.query(ProductLine).count()
    logger.info(f"ProductLine count: {count}")
    return count
