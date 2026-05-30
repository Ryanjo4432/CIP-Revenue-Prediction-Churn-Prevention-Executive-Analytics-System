from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Customer
from schemas import CustomerCreate, CustomerOut

router = APIRouter()


@router.post("/", response_model=CustomerOut, status_code=201)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    existing = db.query(Customer).filter(Customer.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="email already exists")

    customer = Customer(**payload.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


@router.get("/", response_model=List[CustomerOut])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Customer).offset(skip).limit(limit).all()


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")
    return customer


@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, payload: CustomerCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)
    return customer


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")

    db.delete(customer)
    db.commit()
