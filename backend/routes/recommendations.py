from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Recommendation
from schemas import RecommendationCreate, RecommendationOut
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../recommendation_engine"))
from rules import generate_recommendations, get_recommendations_for_customer

router = APIRouter()


@router.post("/generate")
def generate():
    try:
        results = generate_recommendations()
        return {"count": len(results), "recommendations": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_all(db: Session = Depends(get_db)):
    rows = db.query(Recommendation).order_by(Recommendation.created_at.desc()).all()
    return rows


@router.get("/customer/{customer_id}")
def get_for_customer(customer_id: int):
    recs = get_recommendations_for_customer(customer_id)
    if not recs:
        raise HTTPException(status_code=404, detail="no recommendations found for this customer")
    return recs


@router.post("/", response_model=RecommendationOut, status_code=201)
def create_recommendation(payload: RecommendationCreate, db: Session = Depends(get_db)):
    rec = Recommendation(**payload.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec
