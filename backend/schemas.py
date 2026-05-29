from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


class CustomerCreate(BaseModel):
    name:      str
    email:     EmailStr
    age:       Optional[int] = None
    location:  Optional[str] = None
    join_date: Optional[date] = None

class CustomerOut(BaseModel):
    customer_id: int
    name:        str
    email:       str
    age:         Optional[int]
    location:    Optional[str]
    join_date:   Optional[date]
    is_active:   bool

    # tells pydantic to read from orm objects not just dicts
    model_config = {"from_attributes": True}


class TransactionCreate(BaseModel):
    customer_id: int
    amount:      Decimal
    category:    Optional[str] = None
    date:        Optional[datetime] = None

class TransactionOut(BaseModel):
    transaction_id: int
    customer_id:    int
    amount:         Decimal
    category:       Optional[str]
    date:           Optional[datetime]

    model_config = {"from_attributes": True}


class PredictionCreate(BaseModel):
    customer_id:        int
    churn_probability:  Optional[float] = None
    revenue_prediction: Optional[Decimal] = None
    clv:                Optional[Decimal] = None

class PredictionOut(BaseModel):
    prediction_id:      int
    customer_id:        int
    churn_probability:  Optional[float]
    revenue_prediction: Optional[Decimal]
    clv:                Optional[Decimal]
    predicted_at:       Optional[datetime]

    model_config = {"from_attributes": True}


class RecommendationCreate(BaseModel):
    customer_id:    int
    recommendation: str
    priority:       Optional[str] = "medium"

class RecommendationOut(BaseModel):
    recommendation_id: int
    customer_id:       int
    recommendation:    str
    priority:          Optional[str]
    created_at:        Optional[datetime]

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type:   str

class LoginRequest(BaseModel):
    username: str
    password: str
