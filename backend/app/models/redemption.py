"""Redemption record model for the later rewards workflow."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.reward import Reward


class Redemption(Base):
    __tablename__ = "redemptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    reward_id: Mapped[int] = mapped_column(ForeignKey("rewards.id"), nullable=False)
    coins_spent: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    reward: Mapped["Reward"] = relationship(back_populates="redemptions")
