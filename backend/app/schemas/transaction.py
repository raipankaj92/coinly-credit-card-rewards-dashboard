"""Transaction API response schemas."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    source_transaction_id: str
    timestamp: datetime
    merchant: str
    category: str | None
    amount: Decimal
    currency: str
    status: str
    payment_method: str
    created_at: datetime


class PaginationResponse(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=100)
    total: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class TransactionListResponse(BaseModel):
    data: list[TransactionResponse]
    pagination: PaginationResponse
