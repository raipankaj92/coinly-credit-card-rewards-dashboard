"""Create the PostgreSQL schema and deterministically seed the supplied source data."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = PROJECT_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import func, insert, select, text

from app.core.database import get_engine
from app.models import Base, Redemption, Reward, Transaction, Wallet
from app.services.normalization import SeedDataError, normalize_transaction

SOURCE_PATH = PROJECT_ROOT / "transactions (2) (1).json"
EXPECTED_RECORD_COUNT = 10_000
INITIAL_WALLET_BALANCE = 2_500
INITIAL_REWARDS = [
    {
        "name": "Amazon Rs. 500 Voucher",
        "description": "Digital Amazon India voucher worth Rs. 500.",
        "coin_cost": 5_000,
        "reward_type": "VOUCHER",
        "active": True,
    },
    {
        "name": "Swiggy Rs. 250 Voucher",
        "description": "Digital Swiggy voucher worth Rs. 250.",
        "coin_cost": 2_750,
        "reward_type": "VOUCHER",
        "active": True,
    },
    {
        "name": "Myntra Rs. 500 Voucher",
        "description": "Digital Myntra voucher worth Rs. 500.",
        "coin_cost": 5_000,
        "reward_type": "VOUCHER",
        "active": True,
    },
    {
        "name": "Cashback Rs. 100",
        "description": "Rs. 100 statement cashback.",
        "coin_cost": 1_200,
        "reward_type": "CASHBACK",
        "active": True,
    },
    {
        "name": "Flipkart Rs. 500 Voucher",
        "description": "Digital Flipkart voucher worth Rs. 500.",
        "coin_cost": 5_000,
        "reward_type": "VOUCHER",
        "active": True,
    },
]


def load_transactions(source_path: Path = SOURCE_PATH) -> list[dict[str, Any]]:
    """Load and fully validate the protected JSON source before touching the database."""
    try:
        payload = json.loads(source_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise RuntimeError(f"Source JSON was not found: {source_path}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Source JSON is invalid: {exc}") from exc

    if not isinstance(payload, list):
        raise RuntimeError("Source JSON must contain a top-level array of transaction objects.")
    if len(payload) != EXPECTED_RECORD_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_RECORD_COUNT} source records, found {len(payload)}."
        )
    return [normalize_transaction(record, index) for index, record in enumerate(payload)]


def source_statistics(transactions: list[dict[str, Any]]) -> dict[str, int]:
    duplicate_counts = Counter(item["source_transaction_id"] for item in transactions)
    statistics = {
        "transactions": len(transactions),
        "duplicate_id_groups": sum(count > 1 for count in duplicate_counts.values()),
        "duplicate_id_records": sum(count for count in duplicate_counts.values() if count > 1),
        "negative_amounts": sum(item["amount"] < 0 for item in transactions),
        "missing_categories": sum(item["category"] is None for item in transactions),
    }
    statistics.update(
        {f"status_{status}": count for status, count in Counter(item["status"] for item in transactions).items()}
    )
    return statistics


def validate_seed(connection, expected: dict[str, int]) -> dict[str, int]:
    """Validate the relational result before the atomic seed transaction commits."""
    transaction_count = connection.scalar(select(func.count()).select_from(Transaction))
    negative_amounts = connection.scalar(
        select(func.count()).select_from(Transaction).where(Transaction.amount < 0)
    )
    missing_categories = connection.scalar(
        select(func.count()).select_from(Transaction).where(Transaction.category.is_(None))
    )
    duplicate_id_groups = connection.scalar(
        select(func.count()).select_from(
            select(Transaction.source_transaction_id)
            .group_by(Transaction.source_transaction_id)
            .having(func.count() > 1)
            .subquery()
        )
    )
    reward_count = connection.scalar(select(func.count()).select_from(Reward))
    wallet_count = connection.scalar(select(func.count()).select_from(Wallet))
    database_status_counts = dict(
        connection.execute(select(Transaction.status, func.count()).group_by(Transaction.status)).all()
    )
    values = {
        "transactions": int(transaction_count or 0),
        "duplicate_id_groups": int(duplicate_id_groups or 0),
        "negative_amounts": int(negative_amounts or 0),
        "missing_categories": int(missing_categories or 0),
        "rewards": int(reward_count or 0),
        "wallets": int(wallet_count or 0),
    }
    expected_values = {
        "transactions": expected["transactions"],
        "duplicate_id_groups": expected["duplicate_id_groups"],
        "negative_amounts": expected["negative_amounts"],
        "missing_categories": expected["missing_categories"],
        "rewards": len(INITIAL_REWARDS),
        "wallets": 1,
    }
    expected_values.update(
        {f"status_{status}": expected[f"status_{status}"] for status in ("SUCCESS", "FAILED", "PENDING")}
    )
    values.update(
        {f"status_{status}": int(database_status_counts.get(status, 0)) for status in ("SUCCESS", "FAILED", "PENDING")}
    )
    mismatches = [
        f"{key}: expected {expected_values[key]}, found {values[key]}"
        for key in expected_values
        if values[key] != expected_values[key]
    ]
    if mismatches:
        raise RuntimeError("Seed validation failed: " + "; ".join(mismatches))
    return values


def seed_database() -> dict[str, int]:
    transactions = load_transactions()
    expected = source_statistics(transactions)
    engine = get_engine()
    Base.metadata.create_all(engine)

    # PostgreSQL TRUNCATE is transactional; a failure rolls back the clean reseed entirely.
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE redemptions, wallets, rewards, transactions RESTART IDENTITY"))
        connection.execute(insert(Transaction), transactions)
        connection.execute(insert(Reward), INITIAL_REWARDS)
        connection.execute(insert(Wallet), [{"id": 1, "coin_balance": INITIAL_WALLET_BALANCE}])
        return validate_seed(connection, expected)


def main() -> None:
    try:
        result = seed_database()
    except SeedDataError as exc:
        raise SystemExit(f"Seed failed: {exc}") from exc
    except RuntimeError as exc:
        raise SystemExit(f"Seed failed: {exc}") from exc

    print("PostgreSQL seed completed successfully.")
    print(f"Transactions inserted: {result['transactions']}")
    print(f"Duplicate source-ID groups preserved: {result['duplicate_id_groups']}")
    print(f"Negative amounts preserved: {result['negative_amounts']}")
    print(f"Missing categories stored as NULL: {result['missing_categories']}")
    print(f"Rewards inserted: {result['rewards']}")
    print(f"Wallet records inserted: {result['wallets']}")


if __name__ == "__main__":
    main()
