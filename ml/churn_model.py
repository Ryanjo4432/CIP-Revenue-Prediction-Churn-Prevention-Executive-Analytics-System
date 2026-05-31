import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import os
import pickle

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost:5432/cip_db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def load_data() -> pd.DataFrame:
    query = """
        SELECT
            c.customer_id,
            c.age,
            c.location,
            c.is_active,
            EXTRACT(DAY FROM NOW() - c.join_date)  AS days_since_join,
            COUNT(t.transaction_id)                AS txn_count,
            COALESCE(SUM(t.amount),   0)           AS total_spent,
            COALESCE(AVG(t.amount),   0)           AS avg_txn,
            COALESCE(MAX(t.amount),   0)           AS max_txn,
            COALESCE(EXTRACT(DAY FROM NOW() - MAX(t.date)), 999) AS days_since_last_txn
        FROM customers c
        LEFT JOIN transactions t ON c.customer_id = t.customer_id
        GROUP BY c.customer_id, c.age, c.location, c.is_active, c.join_date
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df


def build_features(df: pd.DataFrame):
    df = df.copy()
    df["age"].fillna(df["age"].median(), inplace=True)

    # encode location strings to numbers so the model can use them
    le = LabelEncoder()
    df["location_enc"] = le.fit_transform(df["location"].fillna("unknown"))

    features = ["age", "location_enc", "days_since_join",
                "txn_count", "total_spent", "avg_txn", "max_txn", "days_since_last_txn"]

    X = df[features]
    # churn = not active, thats our label
    y = (~df["is_active"]).astype(int)
    return X, y, df, le


def train(save_path: str = "/app/churn_model.pkl"):
    df = load_data()
    X, y, _, le = build_features(df)

    if len(df) < 10:
        print("not enough data to train, need at least 10 customers")
        return None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)

    print(classification_report(y_test, model.predict(X_test), zero_division=0))

    with open(save_path, "wb") as f:
        pickle.dump({"model": model, "label_encoder": le}, f)

    print(f"model saved to {save_path}")
    return model


def predict_all(save_path: str = "/app/churn_model.pkl") -> list:
    if not os.path.exists(save_path):
        train(save_path)

    with open(save_path, "rb") as f:
        bundle = pickle.load(f)

    model = bundle["model"]
    le    = bundle["label_encoder"]

    df = load_data()
    X, _, df, _ = build_features(df)

    # known_classes handles if a location wasnt in training data
    known_classes = set(le.classes_)
    df["location_enc"] = df["location"].fillna("unknown").apply(
        lambda x: le.transform([x])[0] if x in known_classes else 0
    )
    X = df[["age", "location_enc", "days_since_join",
            "txn_count", "total_spent", "avg_txn", "max_txn", "days_since_last_txn"]]

    probs = model.predict_proba(X)[:, 1]
    df["churn_probability"] = probs

    results = []
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(text("""
                INSERT INTO predictions (customer_id, churn_probability)
                VALUES (:cid, :prob)
                ON CONFLICT DO NOTHING
            """), {"cid": int(row["customer_id"]), "prob": float(row["churn_probability"])})

            results.append({
                "customer_id":       int(row["customer_id"]),
                "churn_probability": round(float(row["churn_probability"]), 4),
            })

    return results


def predict_one(customer_id: int, save_path: str = "/app/churn_model.pkl") -> dict:
    all_preds = predict_all(save_path)
    match = next((p for p in all_preds if p["customer_id"] == customer_id), None)
    if not match:
        return {"error": "customer not found"}
    return match


if __name__ == "__main__":
    train()
