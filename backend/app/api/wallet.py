"""Wallet endpoint."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.wallet_repository import WalletRepository
from app.schemas.wallet import WalletResponse

router = APIRouter(prefix="/api/wallet", tags=["wallet"])


@router.get("", response_model=WalletResponse)
def get_wallet(session: Session = Depends(get_db)) -> WalletResponse:
    wallet = WalletRepository.get_wallet(session)
    if wallet is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Demo wallet not found.")
    return WalletResponse.model_validate(wallet)
