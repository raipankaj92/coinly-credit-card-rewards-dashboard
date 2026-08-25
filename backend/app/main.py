"""Coinly FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import analytics, rewards, transactions, wallet

app = FastAPI(title="Coinly API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(transactions.router)
app.include_router(wallet.router)
app.include_router(rewards.router)
app.include_router(analytics.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Coinly API"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}
