from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import Order
from schemas.order_schemas import OrderCreate, OrderUpdate
from logger import get_logger

logger = get_logger(__name__)


def get_orderss(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching orders: skip={skip}, limit={limit}")
    return db.query(Order).offset(skip).limit(limit).all()


def get_orders(db: Session, id: int):
    logger.info(f"Fetching order: {id}")
    order = db.query(Order).filter(Order.orderNumber == id).first()
    if not order:
        logger.warning(f"Order not found: {id}")
        raise HTTPException(status_code=404, detail=f"Order {id} not found")
    return order


def create_orders(db: Session, data: OrderCreate):
    logger.info(f"Creating order: {data.orderNumber}")
    try:
        order = Order(**data.model_dump())
        db.add(order)
        db.commit()
        db.refresh(order)
        logger.info(f"Order created: {order.orderNumber}")
        return order
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK error creating order: {e}")
        raise HTTPException(status_code=422, detail="Invalid customerNumber foreign key")


def update_orders(db: Session, id: int, data: OrderUpdate):
    logger.info(f"Updating order: {id}")
    order = get_orders(db, id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    logger.info(f"Order updated: {id}")
    return order


def delete_orders(db: Session, id: int):
    logger.info(f"Deleting order: {id}")
    order = get_orders(db, id)
    try:
        db.delete(order)
        db.commit()
        logger.info(f"Order deleted: {id}")
        return {"detail": "Order deleted"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Cannot delete; order details still reference this order")


def get_orders_with_orderdetails(db: Session, id: int):
    logger.info(f"Fetching order with details: {id}")
    return get_orders(db, id)


def get_orders_by_customer(db: Session, customer_id: int):
    logger.info(f"Fetching orders for customer: {customer_id}")
    return db.query(Order).filter(Order.customerNumber == customer_id).all()


# --- Count ---
def get_orders_count(db: Session) -> int:
    count = db.query(Order).count()
    logger.info(f"Order count: {count}")
    return count
