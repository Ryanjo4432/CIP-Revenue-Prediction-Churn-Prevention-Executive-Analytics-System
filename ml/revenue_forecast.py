import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.linear_model import LinearRegression
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost:5432/cip_db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def load_monthly_revenue() -> pd.DataFrame:
    query = """
        SELECT
            DATE_TRUNC('month', date) AS month,
            SUM(amount)               AS revenue
        FROM transactions
        GROUP BY month
        ORDER BY month
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    df["month"] = pd.to_datetime(df["month"])
    df["revenue"] = df["revenue"].astype(float)
    return df


def forecast(months_ahead: int = 3) -> dict:
    df = load_monthly_revenue()

    if len(df) < 2:
        return {"error": "need at least 2 months of data to forecast"}

    # convert months to integers so linear regression can use them
    df["month_index"] = np.arange(len(df))

    X = df[["month_index"]]
    y = df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    last_index = df["month_index"].max()
    future_indexes = np.arange(last_index + 1, last_index + 1 + months_ahead).reshape(-1, 1)
    predictions = model.predict(future_indexes)

    last_month = df["month"].max()
    future_months = pd.date_range(start=last_month + pd.DateOffset(months=1), periods=months_ahead, freq="MS")

    forecast_data = [
        {
            "month":            str(m)[:7],
            "predicted_revenue": round(float(p), 2),
        }
        for m, p in zip(future_months, predictions)
    ]

    historical = [
        {"month": str(row.month)[:7], "revenue": round(row.revenue, 2)}
        for _, row in df.iterrows()
    ]

    return {
        "historical":      historical,
        "forecast":        forecast_data,
        "trend":           "up" if model.coef_[0] > 0 else "down",
        "monthly_growth":  round(float(model.coef_[0]), 2),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(forecast(3), indent=2))
