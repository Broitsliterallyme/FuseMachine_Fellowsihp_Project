import asyncio
import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import (
    customer_crud, order_crud, product_crud, employee_crud,
    office_crud, payment_crud, orderdetail_crud, productline_crud
)
from logger import get_logger

logger = get_logger(__name__)
router = APIRouter()



@router.get("/customers/count")
def customers_count(db: Session = Depends(get_db)):
    logger.info("GET /customers/count (dashboard)")
    count = customer_crud.get_customers_count(db)
    logger.info(f"Response: customers={count}")
    return {"table": "customers", "count": count}


@router.get("/orders/count")
def orders_count(db: Session = Depends(get_db)):
    logger.info("GET /orders/count (dashboard)")
    count = order_crud.get_orders_count(db)
    logger.info(f"Response: orders={count}")
    return {"table": "orders", "count": count}


@router.get("/products/count")
def products_count(db: Session = Depends(get_db)):
    logger.info("GET /products/count (dashboard)")
    count = product_crud.get_products_count(db)
    logger.info(f"Response: products={count}")
    return {"table": "products", "count": count}


@router.get("/employees/count")
def employees_count(db: Session = Depends(get_db)):
    logger.info("GET /employees/count (dashboard)")
    count = employee_crud.get_employees_count(db)
    logger.info(f"Response: employees={count}")
    return {"table": "employees", "count": count}


@router.get("/offices/count")
def offices_count(db: Session = Depends(get_db)):
    logger.info("GET /offices/count (dashboard)")
    count = office_crud.get_offices_count(db)
    logger.info(f"Response: offices={count}")
    return {"table": "offices", "count": count}


@router.get("/payments/count")
def payments_count(db: Session = Depends(get_db)):
    logger.info("GET /payments/count (dashboard)")
    count = payment_crud.get_payments_count(db)
    logger.info(f"Response: payments={count}")
    return {"table": "payments", "count": count}


@router.get("/orderdetails/count")
def orderdetails_count(db: Session = Depends(get_db)):
    logger.info("GET /orderdetails/count (dashboard)")
    count = orderdetail_crud.get_orderdetails_count(db)
    logger.info(f"Response: orderdetails={count}")
    return {"table": "orderdetails", "count": count}


@router.get("/productlines/count")
def productlines_count(db: Session = Depends(get_db)):
    logger.info("GET /productlines/count (dashboard)")
    count = productline_crud.get_productlines_count(db)
    logger.info(f"Response: productlines={count}")
    return {"table": "productlines", "count": count}



@router.get("/overall_counts")
async def overall_counts(db: Session = Depends(get_db)):
    """
    Returns row counts from all 8 tables simultaneously using asyncio.gather().
    Implements Factor VIII: Concurrency from the Twelve-Factor App.
    """
    logger.info("GET /overall_counts - starting concurrent DB queries")
    start_time = time.perf_counter()

    # Wrap synchronous DB calls as coroutines via run_in_executor
    loop = asyncio.get_event_loop()

    async def count(fn, db):
        return await loop.run_in_executor(None, fn, db)

    logger.info("Launching all 8 count tasks simultaneously via asyncio.gather()")

    (
        customers,
        orders,
        products,
        employees,
        offices,
        payments,
        orderdetails,
        productlines,
    ) = await asyncio.gather(
        count(customer_crud.get_customers_count, db),
        count(order_crud.get_orders_count, db),
        count(product_crud.get_products_count, db),
        count(employee_crud.get_employees_count, db),
        count(office_crud.get_offices_count, db),
        count(payment_crud.get_payments_count, db),
        count(orderdetail_crud.get_orderdetails_count, db),
        count(productline_crud.get_productlines_count, db),
    )

    elapsed = time.perf_counter() - start_time
    logger.info(f"asyncio.gather() completed in {elapsed:.4f}s")

    result = {
        "customers": customers,
        "orders": orders,
        "products": products,
        "employees": employees,
        "offices": offices,
        "payments": payments,
        "orderdetails": orderdetails,
        "productlines": productlines,
    }
    logger.info(f"overall_counts response: {result}")
    return result
