from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from churn_model import predict_all, predict_one, train
from revenue_forecast import forecast
from clv_model import predict_clv

app = FastAPI(title="CIP ML Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "ml"}


@app.post("/train/churn")
def train_churn():
    try:
        train()
        return {"message": "churn model trained and saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/churn")
def churn_all():
    try:
        results = predict_all()
        return {"count": len(results), "predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/churn/{customer_id}")
def churn_one(customer_id: int):
    result = predict_one(customer_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@app.get("/predict/clv")
def clv():
    try:
        results = predict_clv()
        return {"count": len(results), "predictions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/forecast")
def revenue_forecast(months_ahead: int = 3):
    try:
        # months_ahead capped so nobody asks for 100 years of fake data
        months_ahead = min(max(months_ahead, 1), 12)
        result = forecast(months_ahead)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/predict/all/{customer_id}")
def predict_everything(customer_id: int):
    churn = predict_one(customer_id)
    clv_all = predict_clv()
    clv_match = next((c for c in clv_all if c["customer_id"] == customer_id), None)

    return {
        "customer_id": customer_id,
        "churn":       churn,
        "clv":         clv_match,
    }
