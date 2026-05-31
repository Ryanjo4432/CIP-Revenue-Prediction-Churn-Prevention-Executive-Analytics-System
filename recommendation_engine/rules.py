from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@localhost:5432/cip_db")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def _get_latest_predictions(conn) -> list:
    rows = conn.execute(text("""
        SELECT DISTINCT ON (customer_id)
            customer_id, churn_probability, clv
        FROM predictions
        ORDER BY customer_id, predicted_at DESC
    """)).fetchall()
    return rows


def _apply_rules(churn_prob: float, clv: float) -> list:
    actions = []

    churn = churn_prob or 0.0
    value = clv or 0.0

    # high churn rules
    if churn >= 0.70:
        actions.append(("send retention email with 20% discount code", "high"))
    if churn >= 0.85:
        actions.append(("escalate to account manager for personal outreach", "high"))
    if churn >= 0.70 and value >= 2000:
        actions.append(("offer free premium upgrade for 3 months", "high"))

    # mid churn rules
    if 0.40 <= churn < 0.70:
        actions.append(("send re-engagement email with product highlights", "medium"))
    if 0.40 <= churn < 0.70 and value >= 500:
        actions.append(("invite to exclusive webinar or loyalty program", "medium"))

    # low churn high value rules
    if churn < 0.40 and value >= 5000:
        actions.append(("send thank you gift + early access to new features", "low"))
    if churn < 0.40 and value >= 2000:
        actions.append(("upsell to enterprise plan", "low"))

    # no spend rules
    if value == 0 and churn < 0.40:
        actions.append(("send onboarding tips, customer hasnt spent yet", "medium"))

    if not actions:
        actions.append(("monitor customer, no action needed right now", "low"))

    return actions


def generate_recommendations() -> list:
    results = []

    with engine.begin() as conn:
        predictions = _get_latest_predictions(conn)

        # clear old ones before writing fresh batch
        conn.execute(text("DELETE FROM recommendations"))

        for row in predictions:
            customer_id = row.customer_id
            churn_prob  = float(row.churn_probability or 0)
            clv         = float(row.clv or 0)

            actions = _apply_rules(churn_prob, clv)

            for recommendation, priority in actions:
                conn.execute(text("""
                    INSERT INTO recommendations (customer_id, recommendation, priority)
                    VALUES (:cid, :rec, :pri)
                """), {"cid": customer_id, "rec": recommendation, "pri": priority})

                results.append({
                    "customer_id":     customer_id,
                    "churn_probability": round(churn_prob, 4),
                    "clv":             round(clv, 2),
                    "recommendation":  recommendation,
                    "priority":        priority,
                })

    return sorted(results, key=lambda x: (x["priority"] == "high", x["churn_probability"]), reverse=True)


def get_recommendations_for_customer(customer_id: int) -> list:
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT recommendation, priority, created_at
            FROM recommendations
            WHERE customer_id = :cid
            ORDER BY created_at DESC
        """), {"cid": customer_id}).fetchall()

    return [
        {"recommendation": r.recommendation, "priority": r.priority, "created_at": str(r.created_at)}
        for r in rows
    ]
