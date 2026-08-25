"""Wallet API response schema."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WalletResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    coin_balance: int
    updated_at: datetime
