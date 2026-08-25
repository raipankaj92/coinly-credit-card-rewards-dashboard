"""Live PostgreSQL integration tests; skipped when DATABASE_URL is not configured."""

from __future__ import annotations

import os
import sys
import unittest
from decimal import Decimal
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.database import get_engine, get_session_factory
from app.main import app
from app.models import Reward
from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.transaction_repository import TransactionQuery, TransactionRepository
from app.repositories.wallet_repository import WalletRepository
from app.services.reward_service import InsufficientBalanceError, RewardNotFoundError, RewardService


@unittest.skipUnless(os.getenv("DATABASE_URL"), "DATABASE_URL is required for live PostgreSQL integration tests")
class ApiDatabaseIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.session_factory = get_session_factory()

    def test_transaction_pagination_and_status_filtering(self) -> None:
        with self.session_factory() as session:
            records, total = TransactionRepository.list_page(
                session,
                TransactionQuery(page=1, page_size=3, status="SUCCESS", sort_by="timestamp", sort_order="desc"),
            )
        self.assertEqual(total, 8_800)
        self.assertEqual(len(records), 3)
        self.assertTrue(all(record.status == "SUCCESS" for record in records))

    def test_analytics_are_database_aggregations(self) -> None:
        with self.session_factory() as session:
            categories = AnalyticsRepository.category_spending(session)
            months = AnalyticsRepository.monthly_spending(session)
        self.assertTrue(categories)
        self.assertTrue(months)
        self.assertTrue(all(category and isinstance(total, Decimal) for category, total in categories))
        self.assertTrue(all(len(month) == 7 and isinstance(total, Decimal) for month, total in months))

    def test_nonexistent_reward_is_rejected(self) -> None:
        with self.session_factory() as session:
            with self.assertRaises(RewardNotFoundError):
                RewardService.redeem_reward(session, 999_999_999)

    def test_insufficient_balance_is_rejected(self) -> None:
        with self.session_factory() as session:
            wallet = WalletRepository.get_wallet(session)
            self.assertIsNotNone(wallet)
            reward = session.scalar(select(Reward).where(Reward.coin_cost > wallet.coin_balance).limit(1))
        if reward is None:
            self.skipTest("No active reward costs more than the demo wallet balance.")

        with self.session_factory() as session:
            with self.assertRaises(InsufficientBalanceError):
                RewardService.redeem_reward(session, reward.id)

    def test_successful_redemption_rolls_back_after_verification(self) -> None:
        with self.session_factory() as session:
            wallet = WalletRepository.get_wallet(session)
            self.assertIsNotNone(wallet)
            reward = session.scalar(
                select(Reward)
                .where(Reward.active.is_(True), Reward.coin_cost <= wallet.coin_balance)
                .order_by(Reward.coin_cost)
                .limit(1)
            )
        if reward is None:
            self.skipTest("No active reward is affordable for the demo wallet.")

        connection = get_engine().connect()
        outer_transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint", expire_on_commit=False)
        try:
            result = RewardService.redeem_reward(session, reward.id)
            self.assertIsNotNone(result.redemption.id)
            self.assertEqual(result.updated_balance, wallet.coin_balance - reward.coin_cost)
            self.assertEqual(result.redemption.coins_spent, reward.coin_cost)
        finally:
            session.close()
            outer_transaction.rollback()
            connection.close()


class ApiWiringTests(unittest.TestCase):
    def test_expected_routes_are_registered(self) -> None:
        routes = set(app.openapi()["paths"])
        self.assertTrue(
            {"/", "/health", "/api/transactions", "/api/transactions/{transaction_id}", "/api/wallet", "/api/rewards", "/api/rewards/{reward_id}/redeem", "/api/analytics/summary", "/api/analytics/category-spending", "/api/analytics/monthly-spending"}.issubset(routes)
        )


if __name__ == "__main__":
    unittest.main()
