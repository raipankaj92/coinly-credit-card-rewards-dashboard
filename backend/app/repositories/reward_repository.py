"""Reward catalogue query operations."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Reward


class RewardRepository:
    @staticmethod
    def list_active(session: Session) -> list[Reward]:
        return list(session.scalars(select(Reward).where(Reward.active.is_(True)).order_by(Reward.id)))

    @staticmethod
    def get_active_by_id(session: Session, reward_id: int) -> Reward | None:
        return session.scalar(select(Reward).where(Reward.id == reward_id, Reward.active.is_(True)))
