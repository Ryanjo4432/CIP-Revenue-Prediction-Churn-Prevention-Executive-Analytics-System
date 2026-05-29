from sqlalchemy import Column, Integer, String, Float, Numeric, Boolean, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    email       = Column(String(150), unique=True, nullable=False)
    age         = Column(Integer)
    location    = Column(String(100))
    join_date   = Column(Date, server_default=func.current_date())
    is_active   = Column(Boolean, default=True)

    transactions    = relationship("Transaction",    back_populates="customer", cascade="all, delete")
    predictions     = relationship("Prediction",     back_populates="customer", cascade="all, delete")
    recommendations = relationship("Recommendation", back_populates="customer", cascade="all, delete")


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    customer_id    = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    amount         = Column(Numeric(12, 2), nullable=False)
    category       = Column(String(50))
    date           = Column(DateTime, server_default=func.now())

    customer = relationship("Customer", back_populates="transactions")


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id      = Column(Integer, primary_key=True, index=True)
    customer_id        = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    churn_probability  = Column(Float)
    revenue_prediction = Column(Numeric(12, 2))
    clv                = Column(Numeric(12, 2))
    predicted_at       = Column(DateTime, server_default=func.now())

    customer = relationship("Customer", back_populates="predictions")


class Recommendation(Base):
    __tablename__ = "recommendations"

    recommendation_id = Column(Integer, primary_key=True, index=True)
    customer_id       = Column(Integer, ForeignKey("customers.customer_id", ondelete="CASCADE"), nullable=False)
    recommendation    = Column(Text, nullable=False)
    priority          = Column(String(20), default="medium")
    created_at        = Column(DateTime, server_default=func.now())

    customer = relationship("Customer", back_populates="recommendations")
