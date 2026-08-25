"""PostgreSQL aggregation queries for dashboard charts."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import func, literal, select
from sqlalchemy.orm import Session

from app.models import Transaction


class AnalyticsRepository:
    @staticmethod
    def dashboard_summary(session: Session) -> tuple[Decimal, int, int]:
        statement = select(
            func.coalesce(func.sum(Transaction.amount), 0),
            func.count(Transaction.id).filter(Transaction.status == "SUCCESS"),
            func.count(Transaction.id),
        )
        total, successful, count = session.execute(statement).one()
        return Decimal(total), int(successful), int(count)

    @staticmethod
    def category_spending(session: Session) -> list[tuple[str, Decimal]]:
        category = func.coalesce(Transaction.category, literal("Uncategorized")).label("category")
        total = func.sum(Transaction.amount).label("total")
        statement = select(category, total).group_by(category).order_by(total.desc(), category.asc())
        return [(str(name), Decimal(amount)) for name, amount in session.execute(statement).all()]

    @staticmethod
    def monthly_spending(session: Session) -> list[tuple[str, Decimal]]:
        month = func.date_trunc("month", Transaction.timestamp).label("month")
        total = func.sum(Transaction.amount).label("total")
        statement = select(month, total).group_by(month).order_by(month.asc())
        return [(bucket.strftime("%Y-%m"), Decimal(amount)) for bucket, amount in session.execute(statement).all()]
