"""Reward catalogue and redemption response schemas."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class RewardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    coin_cost: int
    reward_type: str
    active: bool


class RedemptionResponse(BaseModel):
    redemption_id: int
    reward: RewardResponse
    updated_balance: int
