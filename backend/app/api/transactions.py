"""Transaction browsing endpoints."""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.transaction_repository import TransactionQuery
from app.schemas.transaction import PaginationResponse, TransactionListResponse, TransactionResponse
from app.services.transaction_service import (
    TransactionService,
    TransactionValidationError,
    parse_datetime_boundary,
)

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("", response_model=TransactionListResponse)
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    search: str | None = None,
    category: str | None = None,
    status_filter: Literal["SUCCESS", "FAILED", "PENDING"] | None = Query(None, alias="status"),
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    sort_by: Literal["timestamp", "amount"] = "timestamp",
    sort_order: Literal["asc", "desc"] = "desc",
    session: Session = Depends(get_db),
) -> TransactionListResponse:
    try:
        query = TransactionQuery(
            page=page,
            page_size=page_size,
            search=search,
            category=category,
            status=status_filter,
            min_amount=min_amount,
            max_amount=max_amount,
            start_date=parse_datetime_boundary(start_date, end_of_day=False),
            end_date=parse_datetime_boundary(end_date, end_of_day=True),
            sort_by=sort_by,
            sort_order=sort_order,
        )
        records, total = TransactionService.list_transactions(session, query)
    except TransactionValidationError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    total_pages = (total + page_size - 1) // page_size if total else 0
    return TransactionListResponse(
        data=[TransactionResponse.model_validate(record) for record in records],
        pagination=PaginationResponse(
            page=page, page_size=page_size, total=total, total_pages=total_pages
        ),
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, session: Session = Depends(get_db)) -> TransactionResponse:
    record = TransactionService.get_transaction(session, transaction_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found.")
    return TransactionResponse.model_validate(record)
