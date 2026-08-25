"""Atomic reward-redemption business rules."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.models import Redemption, Reward
from app.repositories.reward_repository import RewardRepository
from app.repositories.wallet_repository import WalletRepository


class RewardNotFoundError(LookupError):
    pass


class WalletNotFoundError(LookupError):
    pass


class InsufficientBalanceError(ValueError):
    pass


@dataclass(frozen=True)
class RedemptionResult:
    redemption: Redemption
    reward: Reward
    updated_balance: int


class RewardService:
    @staticmethod
    def list_active_rewards(session: Session) -> list[Reward]:
        return RewardRepository.list_active(session)

    @staticmethod
    def redeem_reward(session: Session, reward_id: int) -> RedemptionResult:
        """Lock the wallet, deduct coins, and insert a redemption as one transaction."""
        with session.begin():
            reward = RewardRepository.get_active_by_id(session, reward_id)
            if reward is None:
                raise RewardNotFoundError("Reward does not exist or is inactive.")

            wallet = WalletRepository.get_wallet_for_update(session)
            if wallet is None:
                raise WalletNotFoundError("Demo wallet does not exist.")
            if wallet.coin_balance < reward.coin_cost:
                raise InsufficientBalanceError("Insufficient coin balance for this reward.")

            wallet.coin_balance -= reward.coin_cost
            redemption = Redemption(reward_id=reward.id, coins_spent=reward.coin_cost)
            session.add(redemption)
            session.flush()
            session.refresh(wallet)
            return RedemptionResult(
                redemption=redemption,
                reward=reward,
                updated_balance=wallet.coin_balance,
            )
