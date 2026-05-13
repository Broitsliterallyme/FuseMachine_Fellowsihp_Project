from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Customer, Order, Payment
from schemas.customer_schemas import CustomerCreate, CustomerUpdate
from logger import get_logger

logger = get_logger(__name__)


def get_customers(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching customers: skip={skip}, limit={limit}")
    return db.query(Customer).offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int):
    logger.info(f"Fetching customer ID={customer_id}")
    customer = db.query(Customer).filter(Customer.customerNumber == customer_id).first()
    if not customer:
        logger.warning(f"Customer not found: ID={customer_id}")
        raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
    return customer


def create_customer(db: Session, data: CustomerCreate):
    logger.info(f"Creating customer: {data.customerNumber}")
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    logger.info(f"Customer created: {customer.customerNumber}")
    return customer


def update_customer(db: Session, customer_id: int, data: CustomerUpdate):
    logger.info(f"Updating customer ID={customer_id}")
    customer = get_customer(db, customer_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    logger.info(f"Customer updated: ID={customer_id}")
    return customer


def delete_customer(db: Session, customer_id: int):
    logger.info(f"Deleting customer ID={customer_id}")
    customer = get_customer(db, customer_id)
    db.delete(customer)
    db.commit()
    logger.info(f"Customer deleted: ID={customer_id}")
    return {"detail": "Customer deleted"}


def get_customer_orders(db: Session, customer_id: int):
    logger.info(f"Fetching orders for customer ID={customer_id}")
    get_customer(db, customer_id)
    return db.query(Order).filter(Order.customerNumber == customer_id).all()


def get_customer_payments(db: Session, customer_id: int):
    logger.info(f"Fetching payments for customer ID={customer_id}")
    get_customer(db, customer_id)
    return db.query(Payment).filter(Payment.customerNumber == customer_id).all()


# --- Count for Task 3 ---
def get_customers_count(db: Session) -> int:
    count = db.query(Customer).count()
    logger.info(f"Customer count: {count}")
    return count
