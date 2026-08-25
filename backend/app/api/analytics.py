"""Read-only dashboard analytics endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.analytics import CategorySpendingResponse, DashboardSummaryResponse, MonthlySpendingResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def dashboard_summary(session: Session = Depends(get_db)) -> DashboardSummaryResponse:
    total, successful, count = AnalyticsService.dashboard_summary(session)
    return DashboardSummaryResponse(total_spending=total, successful_transactions=successful, transaction_count=count)


@router.get("/category-spending", response_model=list[CategorySpendingResponse])
def category_spending(session: Session = Depends(get_db)) -> list[CategorySpendingResponse]:
    return [
        CategorySpendingResponse(category=category, total=total)
        for category, total in AnalyticsService.category_spending(session)
    ]


@router.get("/monthly-spending", response_model=list[MonthlySpendingResponse])
def monthly_spending(session: Session = Depends(get_db)) -> list[MonthlySpendingResponse]:
    return [
        MonthlySpendingResponse(month=month, total=total)
        for month, total in AnalyticsService.monthly_spending(session)
    ]
