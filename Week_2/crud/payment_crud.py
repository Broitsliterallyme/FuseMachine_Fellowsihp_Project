from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import Payment
from schemas.payment_schemas import PaymentCreate, PaymentUpdate
from logger import get_logger

logger = get_logger(__name__)


def get_paymentss(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching payments: skip={skip}, limit={limit}")
    return db.query(Payment).offset(skip).limit(limit).all()


def get_payments(db: Session, customer_number: int, check_number: str):
    logger.info(f"Fetching payment: customerNumber={customer_number}, checkNumber={check_number}")
    payment = db.query(Payment).filter(
        Payment.customerNumber == customer_number,
        Payment.checkNumber == check_number
    ).first()
    if not payment:
        logger.warning(f"Payment not found: {customer_number}/{check_number}")
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


def create_payments(db: Session, data: PaymentCreate):
    logger.info(f"Creating payment: {data.customerNumber}/{data.checkNumber}")
    try:
        payment = Payment(**data.model_dump())
        db.add(payment)
        db.commit()
        db.refresh(payment)
        logger.info(f"Payment created: {payment.customerNumber}/{payment.checkNumber}")
        return payment
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK error creating payment: {e}")
        raise HTTPException(status_code=422, detail="Invalid customerNumber foreign key")


def update_payments(db: Session, customer_number: int, check_number: str, data: PaymentUpdate):
    logger.info(f"Updating payment: {customer_number}/{check_number}")
    payment = get_payments(db, customer_number, check_number)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(payment, field, value)
    db.commit()
    db.refresh(payment)
    logger.info(f"Payment updated: {customer_number}/{check_number}")
    return payment


def delete_payments(db: Session, customer_number: int, check_number: str):
    logger.info(f"Deleting payment: {customer_number}/{check_number}")
    payment = get_payments(db, customer_number, check_number)
    db.delete(payment)
    db.commit()
    logger.info(f"Payment deleted: {customer_number}/{check_number}")
    return {"detail": "Payment deleted"}


def get_payments_by_customer(db: Session, customer_number: int):
    logger.info(f"Fetching payments for customer: {customer_number}")
    return db.query(Payment).filter(Payment.customerNumber == customer_number).all()


# --- Count ---
def get_payments_count(db: Session) -> int:
    count = db.query(Payment).count()
    logger.info(f"Payment count: {count}")
    return count
