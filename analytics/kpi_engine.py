import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timedelta


def get_monthly_revenue(db: Session) -> dict:
    rows = db.execute(text("""
        SELECT
            DATE_TRUNC('month', date) AS month,
            SUM(amount)              AS revenue
        FROM transactions
        GROUP BY month
        ORDER BY month
    """)).fetchall()

    return [
        {"month": str(r.month)[:7], "revenue": float(r.revenue)}
        for r in rows
    ]


def get_avg_order_value(db: Session) -> float:
    result = db.execute(text("SELECT AVG(amount) FROM transactions")).scalar()
    return round(float(result or 0), 2)


def get_total_revenue(db: Session) -> float:
    result = db.execute(text("SELECT SUM(amount) FROM transactions")).scalar()
    return round(float(result or 0), 2)


def get_churn_rate(db: Session) -> float:
    total    = db.execute(text("SELECT COUNT(*) FROM customers")).scalar()
    inactive = db.execute(text("SELECT COUNT(*) FROM customers WHERE is_active = false")).scalar()
    if total == 0:
        return 0.0
    return round((inactive / total) * 100, 2)


def get_retention_rate(db: Session) -> float:
    return round(100 - get_churn_rate(db), 2)


def get_customer_lifetime_value(db: Session) -> float:
    # avg revenue per customer * estimated lifespan in months
    result = db.execute(text("""
        SELECT AVG(total) FROM (
            SELECT customer_id, SUM(amount) AS total
            FROM transactions
            GROUP BY customer_id
        ) sub
    """)).scalar()

    avg_spend = float(result or 0)

    avg_months = db.execute(text("""
        SELECT AVG(EXTRACT(MONTH FROM AGE(NOW(), join_date)) + 1)
        FROM customers
    """)).scalar()

    lifespan = float(avg_months or 1)

    # monthly value * projected 24 month lifespan
    monthly = avg_spend / max(lifespan, 1)
    clv = monthly * 24
    return round(clv, 2)


def get_top_customers(db: Session, limit: int = 5) -> list:
    rows = db.execute(text("""
        SELECT c.customer_id, c.name, c.email, SUM(t.amount) AS total_spent
        FROM customers c
        JOIN transactions t ON c.customer_id = t.customer_id
        GROUP BY c.customer_id, c.name, c.email
        ORDER BY total_spent DESC
        LIMIT :limit
    """), {"limit": limit}).fetchall()

    return [
        {"customer_id": r.customer_id, "name": r.name, "email": r.email, "total_spent": float(r.total_spent)}
        for r in rows
    ]


def get_revenue_by_category(db: Session) -> list:
    rows = db.execute(text("""
        SELECT category, SUM(amount) AS total
        FROM transactions
        WHERE category IS NOT NULL
        GROUP BY category
        ORDER BY total DESC
    """)).fetchall()

    return [{"category": r.category, "total": float(r.total)} for r in rows]


def get_full_kpi_report(db: Session) -> dict:
    return {
        "total_revenue":         get_total_revenue(db),
        "avg_order_value":       get_avg_order_value(db),
        "churn_rate":            get_churn_rate(db),
        "retention_rate":        get_retention_rate(db),
        "customer_lifetime_value": get_customer_lifetime_value(db),
        "monthly_revenue":       get_monthly_revenue(db),
        "top_customers":         get_top_customers(db),
        "revenue_by_category":   get_revenue_by_category(db),
    }
