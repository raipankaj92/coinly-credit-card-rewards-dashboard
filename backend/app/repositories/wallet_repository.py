"""Single-wallet query operations, including the redemption lock."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Wallet


class WalletRepository:
    @staticmethod
    def get_wallet(session: Session) -> Wallet | None:
        return session.scalar(select(Wallet).order_by(Wallet.id).limit(1))

    @staticmethod
    def get_wallet_for_update(session: Session) -> Wallet | None:
        return session.scalar(select(Wallet).order_by(Wallet.id).limit(1).with_for_update())
