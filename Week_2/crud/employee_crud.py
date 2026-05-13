from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from models import Employee
from schemas.employee_schemas import EmployeeCreate, EmployeeUpdate
from logger import get_logger

logger = get_logger(__name__)


def get_employeess(db: Session, skip: int = 0, limit: int = 100):
    logger.info(f"Fetching employees: skip={skip}, limit={limit}")
    return db.query(Employee).offset(skip).limit(limit).all()


def get_employees(db: Session, id: int):
    logger.info(f"Fetching employee: {id}")
    emp = db.query(Employee).filter(Employee.employeeNumber == id).first()
    if not emp:
        logger.warning(f"Employee not found: {id}")
        raise HTTPException(status_code=404, detail=f"Employee {id} not found")
    return emp


def create_employees(db: Session, data: EmployeeCreate):
    logger.info(f"Creating employee: {data.employeeNumber}")
    try:
        emp = Employee(**data.model_dump())
        db.add(emp)
        db.commit()
        db.refresh(emp)
        logger.info(f"Employee created: {emp.employeeNumber}")
        return emp
    except IntegrityError as e:
        db.rollback()
        logger.error(f"FK error creating employee: {e}")
        raise HTTPException(status_code=422, detail="Invalid officeCode or reportsTo foreign key")


def update_employees(db: Session, id: int, data: EmployeeUpdate):
    logger.info(f"Updating employee: {id}")
    emp = get_employees(db, id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)
    db.commit()
    db.refresh(emp)
    logger.info(f"Employee updated: {id}")
    return emp


def delete_employees(db: Session, id: int):
    logger.info(f"Deleting employee: {id}")
    emp = get_employees(db, id)
    try:
        db.delete(emp)
        db.commit()
        logger.info(f"Employee deleted: {id}")
        return {"detail": "Employee deleted"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Cannot delete; employee has direct reports or customers assigned")


def get_employees_with_customers(db: Session, id: int):
    logger.info(f"Fetching employee with customers: {id}")
    return get_employees(db, id)


def get_employee_reports(db: Session, id: int):
    logger.info(f"Fetching reports for employee: {id}")
    get_employees(db, id)
    return db.query(Employee).filter(Employee.reportsTo == id).all()


# --- Count ---
def get_employees_count(db: Session) -> int:
    count = db.query(Employee).count()
    logger.info(f"Employee count: {count}")
    return count
