from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Transaction, Customer
from schemas import TransactionCreate, TransactionOut

router = APIRouter()


@router.post("/", response_model=TransactionOut, status_code=201)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == payload.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")

    txn = Transaction(**payload.model_dump())
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


@router.get("/", response_model=List[TransactionOut])
def get_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Transaction).offset(skip).limit(limit).all()


@router.get("/customer/{customer_id}", response_model=List[TransactionOut])
def get_transactions_by_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="customer not found")

    return db.query(Transaction).filter(Transaction.customer_id == customer_id).all()


@router.get("/{transaction_id}", response_model=TransactionOut)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    txn = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="transaction not found")
    return txn


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    txn = db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    if not txn:
        raise HTTPException(status_code=404, detail="transaction not found")

    db.delete(txn)
    db.commit()
