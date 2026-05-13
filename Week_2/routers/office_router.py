from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from crud import office_crud
from schemas.office_schemas import OfficeCreate, OfficeUpdate, OfficeOut
from schemas.employee_schemas import EmployeeOut
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[OfficeOut])
def list_offices(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    logger.info(f"GET /offices skip={skip} limit={limit}")
    return office_crud.get_officess(db, skip=skip, limit=limit)


@router.get("/count")
def count_offices(db: Session = Depends(get_db)):
    logger.info("GET /offices/count")
    return {"table": "offices", "count": office_crud.get_offices_count(db)}


@router.get("/{officeCode}", response_model=OfficeOut)
def get_office(officeCode: str, db: Session = Depends(get_db)):
    logger.info(f"GET /offices/{officeCode}")
    return office_crud.get_offices(db, officeCode)


@router.get("/{officeCode}/employees", response_model=List[EmployeeOut])
def get_office_employees(officeCode: str, db: Session = Depends(get_db)):
    logger.info(f"GET /offices/{officeCode}/employees")
    office = office_crud.get_offices_with_employees(db, officeCode)
    return office.employees or []


@router.post("/", response_model=OfficeOut, status_code=201)
def create_office(data: OfficeCreate, db: Session = Depends(get_db)):
    logger.info(f"POST /offices - {data.officeCode}")
    return office_crud.create_offices(db, data)


@router.put("/{officeCode}", response_model=OfficeOut)
def update_office(officeCode: str, data: OfficeUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /offices/{officeCode}")
    return office_crud.update_offices(db, officeCode, data)


@router.delete("/{officeCode}")
def delete_office(officeCode: str, db: Session = Depends(get_db)):
    logger.info(f"DELETE /offices/{officeCode}")
    return office_crud.delete_offices(db, officeCode)
