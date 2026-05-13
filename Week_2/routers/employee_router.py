from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import employee_crud
from schemas.employee_schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut
from schemas.customer_schemas import CustomerOut
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[EmployeeOut])
def list_employees(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    logger.info(f"GET /employees skip={skip} limit={limit}")
    return employee_crud.get_employeess(db, skip=skip, limit=limit)


@router.get("/count")
def count_employees(db: Session = Depends(get_db)):
    logger.info("GET /employees/count")
    return {"table": "employees", "count": employee_crud.get_employees_count(db)}


@router.get("/{employeeNumber}", response_model=EmployeeOut)
def get_employee(employeeNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /employees/{employeeNumber}")
    return employee_crud.get_employees(db, employeeNumber)


@router.get("/{employeeNumber}/customers", response_model=List[CustomerOut])
def get_employee_customers(employeeNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /employees/{employeeNumber}/customers")
    emp = employee_crud.get_employees_with_customers(db, employeeNumber)
    return emp.customers or []


@router.get("/{employeeNumber}/reports", response_model=List[EmployeeOut])
def get_employee_reports(employeeNumber: int, db: Session = Depends(get_db)):
    logger.info(f"GET /employees/{employeeNumber}/reports")
    return employee_crud.get_employee_reports(db, employeeNumber)


@router.post("/", response_model=EmployeeOut, status_code=201)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /employees - {data.employeeNumber}")
    return employee_crud.create_employees(db, data)


@router.put("/{employeeNumber}", response_model=EmployeeOut)
def update_employee(employeeNumber: int, data: EmployeeUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /employees/{employeeNumber}")
    return employee_crud.update_employees(db, employeeNumber, data)


@router.delete("/{employeeNumber}")
def delete_employee(employeeNumber: int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /employees/{employeeNumber}")
    return employee_crud.delete_employees(db, employeeNumber)
