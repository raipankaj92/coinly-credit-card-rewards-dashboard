"""Transaction use cases and boundary validation."""

from __future__ import annotations

from datetime import UTC, date, datetime, time
from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.transaction_repository import TransactionQuery, TransactionRepository

VALID_STATUSES = {"SUCCESS", "FAILED", "PENDING"}


class TransactionValidationError(ValueError):
    pass


def parse_datetime_boundary(value: str | None, *, end_of_day: bool) -> datetime | None:
    if value is None:
        return None
    try:
        if "T" not in value and " " not in value:
            parsed_date = date.fromisoformat(value)
            return datetime.combine(parsed_date, time.max if end_of_day else time.min, tzinfo=UTC)
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise TransactionValidationError("Dates must be ISO dates or ISO datetimes.") from exc
    return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)


class TransactionService:
    @staticmethod
    def list_transactions(session: Session, query: TransactionQuery):
        if query.status and query.status not in VALID_STATUSES:
            raise TransactionValidationError("status must be SUCCESS, FAILED, or PENDING.")
        if query.min_amount is not None and query.max_amount is not None and query.min_amount > query.max_amount:
            raise TransactionValidationError("min_amount cannot exceed max_amount.")
        records, total = TransactionRepository.list_page(session, query)
        return records, total

    @staticmethod
    def get_transaction(session: Session, transaction_id: int):
        return TransactionRepository.get_by_id(session, transaction_id)
