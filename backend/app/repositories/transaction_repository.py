"""Server-side transaction query operations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models import Transaction


@dataclass(frozen=True)
class TransactionQuery:
    page: int
    page_size: int
    search: str | None = None
    category: str | None = None
    status: str | None = None
    min_amount: Decimal | None = None
    max_amount: Decimal | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    sort_by: str = "timestamp"
    sort_order: str = "desc"


class TransactionRepository:
    _SORTABLE_COLUMNS = {
        "timestamp": Transaction.timestamp,
        "amount": Transaction.amount,
    }

    @staticmethod
    def get_by_id(session: Session, transaction_id: int) -> Transaction | None:
        return session.get(Transaction, transaction_id)

    @classmethod
    def list_page(cls, session: Session, query: TransactionQuery) -> tuple[list[Transaction], int]:
        filters = cls._filters(query)
        total = session.scalar(select(func.count()).select_from(Transaction).where(*filters)) or 0
        sort_column = cls._SORTABLE_COLUMNS[query.sort_by]
        sort_expression = sort_column.asc() if query.sort_order == "asc" else sort_column.desc()
        statement: Select[tuple[Transaction]] = (
            select(Transaction)
            .where(*filters)
            .order_by(sort_expression, Transaction.id.asc())
            .offset((query.page - 1) * query.page_size)
            .limit(query.page_size)
        )
        return list(session.scalars(statement)), int(total)

    @staticmethod
    def _filters(query: TransactionQuery) -> list:
        filters = []
        if query.search:
            term = f"%{query.search.strip()}%"
            filters.append(
                or_(
                    Transaction.merchant.ilike(term),
                    Transaction.source_transaction_id.ilike(term),
                )
            )
        if query.category:
            filters.append(Transaction.category == query.category.strip())
        if query.status:
            filters.append(Transaction.status == query.status)
        if query.min_amount is not None:
            filters.append(Transaction.amount >= query.min_amount)
        if query.max_amount is not None:
            filters.append(Transaction.amount <= query.max_amount)
        if query.start_date is not None:
            filters.append(Transaction.timestamp >= query.start_date)
        if query.end_date is not None:
            filters.append(Transaction.timestamp <= query.end_date)
        return filters
