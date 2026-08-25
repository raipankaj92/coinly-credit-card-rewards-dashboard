"""Analytics response contracts backed by PostgreSQL aggregations."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel


class CategorySpendingResponse(BaseModel):
    category: str
    total: Decimal


class MonthlySpendingResponse(BaseModel):
    month: str
    total: Decimal


class DashboardSummaryResponse(BaseModel):
    total_spending: Decimal
    successful_transactions: int
    transaction_count: int
