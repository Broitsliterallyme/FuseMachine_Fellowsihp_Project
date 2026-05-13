from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import OrderDetail
from schemas.orderdetail_schemas import OrderDetailCreate, OrderDetailUpdate
from logger import get_logger

logger = get_logger(__name__)


def get_orderdetailss(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching order details: skip={skip}, limit={limit}")
    return db.query(OrderDetail).offset(skip).limit(limit).all()


def get_orderdetails(db: Session, order_number: int, product_code: str):
    logger.info(f"Fetching order detail: orderNumber={order_number}, productCode={product_code}")
    od = db.query(OrderDetail).filter(
        OrderDetail.orderNumber == order_number,
        OrderDetail.productCode == product_code
    ).first()
    if not od:
        logger.warning(f"OrderDetail not found: {order_number}/{product_code}")
        raise HTTPException(status_code=404, detail="Order detail not found")
    return od


def create_orderdetails(db: Session, data: OrderDetailCreate):
    logger.info(f"Creating order detail: {data.orderNumber}/{data.productCode}")
    try:
        od = OrderDetail(**data.model_dump())
        db.add(od)
        db.commit()
        db.refresh(od)
        logger.info(f"OrderDetail created: {od.orderNumber}/{od.productCode}")
        return od
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK error creating order detail: {e}")
        raise HTTPException(status_code=422, detail="Invalid orderNumber or productCode foreign key")


def update_orderdetails(db: Session, order_number: int, product_code: str, data: OrderDetailUpdate):
    logger.info(f"Updating order detail: {order_number}/{product_code}")
    od = get_orderdetails(db, order_number, product_code)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(od, field, value)
    db.commit()
    db.refresh(od)
    logger.info(f"OrderDetail updated: {order_number}/{product_code}")
    return od


def delete_orderdetails(db: Session, order_number: int, product_code: str):
    logger.info(f"Deleting order detail: {order_number}/{product_code}")
    od = get_orderdetails(db, order_number, product_code)
    db.delete(od)
    db.commit()
    logger.info(f"OrderDetail deleted: {order_number}/{product_code}")
    return {"detail": "Order detail deleted"}


def get_orderdetails_by_order(db: Session, order_number: int):
    logger.info(f"Fetching details for order: {order_number}")
    return db.query(OrderDetail).filter(OrderDetail.orderNumber == order_number).all()


def get_orderdetails_by_product(db: Session, product_code: str):
    logger.info(f"Fetching details for product: {product_code}")
    return db.query(OrderDetail).filter(OrderDetail.productCode == product_code).all()


# --- Count ---
def get_orderdetails_count(db: Session) -> int:
    count = db.query(OrderDetail).count()
    logger.info(f"OrderDetail count: {count}")
    return count
