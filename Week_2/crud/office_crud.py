from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import Office
from schemas.office_schemas import OfficeCreate, OfficeUpdate
from logger import get_logger

logger = get_logger(__name__)


def get_officess(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching offices: skip={skip}, limit={limit}")
    return db.query(Office).offset(skip).limit(limit).all()


def get_offices(db: Session, id: str):
    logger.info(f"Fetching office: {id}")
    office = db.query(Office).filter(Office.officeCode == id).first()
    if not office:
        logger.warning(f"Office not found: {id}")
        raise HTTPException(status_code=404, detail=f"Office '{id}' not found")
    return office


def create_offices(db: Session, data: OfficeCreate):
    logger.info(f"Creating office: {data.officeCode}")
    office = Office(**data.model_dump())
    db.add(office)
    db.commit()
    db.refresh(office)
    logger.info(f"Office created: {office.officeCode}")
    return office


def update_offices(db: Session, id: str, data: OfficeUpdate):
    logger.info(f"Updating office: {id}")
    office = get_offices(db, id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(office, field, value)
    db.commit()
    db.refresh(office)
    logger.info(f"Office updated: {id}")
    return office


def delete_offices(db: Session, id: str):
    logger.info(f"Deleting office: {id}")
    office = get_offices(db, id)
    try:
        db.delete(office)
        db.commit()
        logger.info(f"Office deleted: {id}")
        return {"detail": "Office deleted"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Cannot delete; employees still reference this office")


def get_offices_with_employees(db: Session, id: str):
    logger.info(f"Fetching office with employees: {id}")
    return get_offices(db, id)


# --- Count ---
def get_offices_count(db: Session) -> int:
    count = db.query(Office).count()
    logger.info(f"Office count: {count}")
    return count
