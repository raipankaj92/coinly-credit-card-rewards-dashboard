"""Model exports and metadata registration."""

from app.models.base import Base
from app.models.redemption import Redemption
from app.models.reward import Reward
from app.models.transaction import Transaction
from app.models.wallet import Wallet

__all__ = ["Base", "Redemption", "Reward", "Transaction", "Wallet"]
