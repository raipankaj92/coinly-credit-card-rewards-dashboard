"""Dashboard analytics use cases."""

from sqlalchemy.orm import Session

from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:
    @staticmethod
    def dashboard_summary(session: Session):
        return AnalyticsRepository.dashboard_summary(session)

    @staticmethod
    def category_spending(session: Session):
        return AnalyticsRepository.category_spending(session)

    @staticmethod
    def monthly_spending(session: Session):
        return AnalyticsRepository.monthly_spending(session)
