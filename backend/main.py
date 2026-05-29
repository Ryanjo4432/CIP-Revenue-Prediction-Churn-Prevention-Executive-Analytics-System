from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
from routes import customers, transactions, predictions, recommendations, analytics, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="CIP API", version="1.0.0", lifespan=lifespan)

# letting react on 3000 talk to this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,            prefix="/auth",            tags=["auth"])
app.include_router(customers.router,       prefix="/customers",       tags=["customers"])
app.include_router(transactions.router,    prefix="/transactions",    tags=["transactions"])
app.include_router(predictions.router,     prefix="/predictions",     tags=["predictions"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
app.include_router(analytics.router,       prefix="/analytics",       tags=["analytics"])

@app.get("/")
def root():
    return {"status": "ok", "message": "CIP API is running"}
