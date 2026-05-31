from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../analytics"))
from kpi_engine import get_full_kpi_report, get_top_customers, get_monthly_revenue, get_revenue_by_category

router = APIRouter()


@router.get("/kpi")
def kpi_report(db: Session = Depends(get_db)):
    return get_full_kpi_report(db)


@router.get("/top-customers")
def top_customers(limit: int = 5, db: Session = Depends(get_db)):
    return get_top_customers(db, limit)


@router.get("/monthly-revenue")
def monthly_revenue(db: Session = Depends(get_db)):
    return get_monthly_revenue(db)


@router.get("/revenue-by-category")
def revenue_by_category(db: Session = Depends(get_db)):
    return get_revenue_by_category(db)
