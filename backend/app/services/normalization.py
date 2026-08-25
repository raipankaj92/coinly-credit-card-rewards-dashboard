"""Strict source-data normalization used by the database seed command."""

from __future__ import annotations

from datetime import UTC, date, datetime, time
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

REQUIRED_TRANSACTION_FIELDS = {
    "id",
    "timestamp",
    "merchant",
    "amount",
    "currency",
    "status",
    "payment_method",
}
VALID_STATUSES = {"SUCCESS", "FAILED", "PENDING"}
MAX_AMOUNT = Decimal("999999999999.99")  # NUMERIC(14,2) maximum.


class SeedDataError(ValueError):
    """Describes an unsafe source value with enough context to repair it."""

    def __init__(self, record_index: int, source_id: object, field: str, message: str):
        self.record_index = record_index
        self.source_id = source_id
        self.field = field
        self.message = message
        super().__init__(
            f"Record {record_index} (source transaction ID {source_id!r}), "
            f"field {field!r}: {message}"
        )


def _error(index: int, source_id: object, field: str, message: str) -> SeedDataError:
    return SeedDataError(index, source_id, field, message)


def normalize_timestamp(value: Any, *, index: int, source_id: object) -> datetime:
    """Normalize supported timestamp formats to an aware UTC datetime."""
    if isinstance(value, bool):
        raise _error(index, source_id, "timestamp", "boolean values are not timestamps")

    if isinstance(value, int):
        if abs(value) < 100_000_000_000:
            raise _error(index, source_id, "timestamp", "numeric timestamps must be epoch milliseconds")
        try:
            return datetime.fromtimestamp(value / 1000, tz=UTC)
        except (OverflowError, OSError, ValueError) as exc:
            raise _error(index, source_id, "timestamp", f"invalid epoch milliseconds: {value!r}") from exc

    if not isinstance(value, str) or not value.strip():
        raise _error(index, source_id, "timestamp", "must be a non-empty string or epoch milliseconds")

    text = value.strip()
    try:
        if "T" in text:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        elif "/" in text:
            parsed = datetime.strptime(text, "%d/%m/%Y %H:%M:%S")
        elif " " in text:
            parsed = datetime.fromisoformat(text)
        else:
            parsed = datetime.combine(date.fromisoformat(text), time.min)
    except ValueError as exc:
        raise _error(index, source_id, "timestamp", f"unsupported timestamp format: {value!r}") from exc

    # The source omits an offset for date-only and local-looking values. Treating those as UTC
    # keeps every stored timestamp timezone-aware without inventing a regional timezone.
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def normalize_amount(value: Any, *, index: int, source_id: object) -> Decimal:
    """Convert JSON number or numeric string to an exact, two-decimal Decimal."""
    if isinstance(value, bool):
        raise _error(index, source_id, "amount", "boolean values are not monetary amounts")
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise _error(index, source_id, "amount", f"invalid decimal value: {value!r}") from exc
    if not amount.is_finite():
        raise _error(index, source_id, "amount", "amount must be finite")
    if amount.as_tuple().exponent < -2:
        raise _error(index, source_id, "amount", "amount has more than two decimal places")
    if abs(amount) > MAX_AMOUNT:
        raise _error(index, source_id, "amount", "amount exceeds NUMERIC(14,2) range")
    return amount.quantize(Decimal("0.01"))


def normalize_status(value: Any, *, index: int, source_id: object) -> str:
    if not isinstance(value, str):
        raise _error(index, source_id, "status", "must be a string")
    status = value.strip().upper()
    if status not in VALID_STATUSES:
        raise _error(index, source_id, "status", f"unsupported status: {value!r}")
    return status


def normalize_optional_category(value: Any, *, index: int, source_id: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise _error(index, source_id, "category", "must be a string or null")
    category = value.strip()
    return category or None


def _required_text(record: Mapping[str, Any], field: str, *, index: int, source_id: object) -> str:
    value = record[field]
    if not isinstance(value, str) or not value.strip():
        raise _error(index, source_id, field, "must be a non-empty string")
    return value.strip()


def normalize_transaction(record: Mapping[str, Any], index: int) -> dict[str, Any]:
    """Validate and normalize a single JSON object for SQLAlchemy bulk insertion."""
    if not isinstance(record, Mapping):
        raise _error(index, None, "record", "must be an object")
    source_id = record.get("id")
    missing = REQUIRED_TRANSACTION_FIELDS - set(record)
    if missing:
        raise _error(index, source_id, "record", f"missing required fields: {', '.join(sorted(missing))}")
    source_id = _required_text(record, "id", index=index, source_id=source_id)
    return {
        "source_transaction_id": source_id,
        "timestamp": normalize_timestamp(record["timestamp"], index=index, source_id=source_id),
        "merchant": _required_text(record, "merchant", index=index, source_id=source_id),
        # The supplied source represents some missing categories by omitting the key.
        "category": normalize_optional_category(record.get("category"), index=index, source_id=source_id),
        "amount": normalize_amount(record["amount"], index=index, source_id=source_id),
        "currency": _required_text(record, "currency", index=index, source_id=source_id).upper(),
        "status": normalize_status(record["status"], index=index, source_id=source_id),
        "payment_method": _required_text(record, "payment_method", index=index, source_id=source_id),
    }
