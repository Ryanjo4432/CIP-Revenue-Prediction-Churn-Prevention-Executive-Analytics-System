import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.linear_model import LinearRegression
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost:5432/cip_db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def load_customer_data() -> pd.DataFrame:
    query = """
        SELECT
            c.customer_id,
            c.name,
            c.age,
            EXTRACT(DAY FROM NOW() - c.join_date)   AS days_as_customer,
            COUNT(t.transaction_id)                 AS txn_count,
            COALESCE(SUM(t.amount),  0)             AS total_spent,
            COALESCE(AVG(t.amount),  0)             AS avg_txn,
            COALESCE(EXTRACT(DAY FROM NOW() - MAX(t.date)), 999) AS days_since_last_txn
        FROM customers c
        LEFT JOIN transactions t ON c.customer_id = t.customer_id
        GROUP BY c.customer_id, c.name, c.age, c.join_date
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df


def predict_clv(projection_months: int = 24) -> list:
    df = load_customer_data()

    df["days_as_customer"]    = df["days_as_customer"].astype(float).fillna(1)
    df["txn_count"]           = df["txn_count"].astype(float)
    df["total_spent"]         = df["total_spent"].astype(float)
    df["avg_txn"]             = df["avg_txn"].astype(float)
    df["days_since_last_txn"] = df["days_since_last_txn"].astype(float)
    df["age"]                 = df["age"].fillna(df["age"].median()).astype(float)

    # monthly spend rate = total spent / months active so far
    df["months_active"] = (df["days_as_customer"] / 30).clip(lower=1)
    df["monthly_spend"] = df["total_spent"] / df["months_active"]

    # recency score: less days since last txn = more likely to keep spending
    df["recency_score"] = 1 / (df["days_since_last_txn"] / 30 + 1)

    df["predicted_clv"] = df["monthly_spend"] * projection_months * df["recency_score"]
    df["predicted_clv"] = df["predicted_clv"].clip(lower=0).round(2)

    results = []
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO predictions (customer_id, clv)
                VALUES (:cid, :clv)
                ON CONFLICT DO NOTHING
            """), {"cid": int(row["customer_id"]), "clv": float(row["predicted_clv"])})

            results.append({
                "customer_id":   int(row["customer_id"]),
                "name":          row["name"],
                "total_spent":   round(float(row["total_spent"]), 2),
                "monthly_spend": round(float(row["monthly_spend"]), 2),
                "predicted_clv": float(row["predicted_clv"]),
                "segment":       _segment(float(row["predicted_clv"])),
            })

    return sorted(results, key=lambda x: x["predicted_clv"], reverse=True)


def _segment(clv: float) -> str:
    # bucket customers so the dashboard can color code them
    if clv >= 5000:
        return "champion"
    elif clv >= 2000:
        return "loyal"
    elif clv >= 500:
        return "potential"
    else:
        return "at-risk"


if __name__ == "__main__":
    import json
    print(json.dumps(predict_clv(), indent=2))
