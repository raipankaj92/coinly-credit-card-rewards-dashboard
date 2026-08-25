"""Focused tests for seed normalization without requiring a database server."""

from __future__ import annotations

import sys
import unittest
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.models import Transaction
from app.services.normalization import (
    normalize_amount,
    normalize_optional_category,
    normalize_status,
    normalize_timestamp,
    normalize_transaction,
)


class NormalizationTests(unittest.TestCase):
    def test_iso_timestamp_normalizes_to_utc(self) -> None:
        result = normalize_timestamp("2025-10-03T21:03:27Z", index=0, source_id="TXN1")
        self.assertEqual(result, datetime(2025, 10, 3, 21, 3, 27, tzinfo=UTC))

    def test_epoch_milliseconds_normalize_to_utc(self) -> None:
        result = normalize_timestamp(1768265109000, index=0, source_id="TXN1")
        self.assertEqual(result, datetime.fromtimestamp(1768265109, tz=UTC))

    def test_date_only_timestamp_uses_utc_midnight(self) -> None:
        result = normalize_timestamp("2025-07-03", index=0, source_id="TXN1")
        self.assertEqual(result, datetime(2025, 7, 3, tzinfo=UTC))

    def test_source_space_separated_timestamp_is_supported(self) -> None:
        result = normalize_timestamp("12/10/2025 16:24:49", index=0, source_id="TXN1")
        self.assertEqual(result, datetime(2025, 10, 12, 16, 24, 49, tzinfo=UTC))

    def test_empty_category_becomes_null(self) -> None:
        self.assertIsNone(normalize_optional_category("", index=0, source_id="TXN1"))
        self.assertIsNone(normalize_optional_category(None, index=0, source_id="TXN1"))

    def test_absent_category_will_be_treated_as_null(self) -> None:
        record = {
            "id": "TXN1",
            "timestamp": "2025-07-03",
            "merchant": "Merchant",
            "amount": 10,
            "currency": "INR",
            "status": "SUCCESS",
            "payment_method": "UPI",
        }
        self.assertIsNone(normalize_transaction(record, 0)["category"])

    def test_numeric_string_amount_becomes_decimal(self) -> None:
        result = normalize_amount("5065.00", index=0, source_id="TXN1")
        self.assertEqual(result, Decimal("5065.00"))

    def test_status_is_normalized(self) -> None:
        self.assertEqual(normalize_status(" success ", index=0, source_id="TXN1"), "SUCCESS")

    def test_duplicate_source_ids_are_not_unique(self) -> None:
        self.assertFalse(Transaction.__table__.c.source_transaction_id.unique)

    def test_negative_amount_is_preserved(self) -> None:
        result = normalize_amount("-53.25", index=0, source_id="TXN1")
        self.assertEqual(result, Decimal("-53.25"))


if __name__ == "__main__":
    unittest.main()
