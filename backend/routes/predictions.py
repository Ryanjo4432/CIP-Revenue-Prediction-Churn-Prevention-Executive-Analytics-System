from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Prediction
from schemas import PredictionCreate, PredictionOut
import httpx
import os

router = APIRouter()

ML_SERVICE_URL = os.getenv("ML_SERVICE_URL", "http://cip_ml:8001")


@router.get("/", response_model=List[PredictionOut])
def get_predictions(db: Session = Depends(get_db)):
    return db.query(Prediction).order_by(Prediction.predicted_at.desc()).all()


@router.get("/customer/{customer_id}", response_model=List[PredictionOut])
def get_predictions_for_customer(customer_id: int, db: Session = Depends(get_db)):
    rows = db.query(Prediction).filter(Prediction.customer_id == customer_id).all()
    if not rows:
        raise HTTPException(status_code=404, detail="no predictions found")
    return rows


@router.post("/run/churn")
def run_churn():
    # calls the ml container over docker network
    try:
        res = httpx.get(f"{ML_SERVICE_URL}/predict/churn", timeout=60)
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ml service unreachable: {str(e)}")


@router.post("/run/clv")
def run_clv():
    try:
        res = httpx.get(f"{ML_SERVICE_URL}/predict/clv", timeout=60)
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ml service unreachable: {str(e)}")


@router.post("/run/forecast")
def run_forecast(months_ahead: int = 3):
    try:
        res = httpx.get(f"{ML_SERVICE_URL}/predict/forecast?months_ahead={months_ahead}", timeout=60)
        return res.json()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ml service unreachable: {str(e)}")


@router.post("/", response_model=PredictionOut, status_code=201)
def create_prediction(payload: PredictionCreate, db: Session = Depends(get_db)):
    pred = Prediction(**payload.model_dump())
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred
