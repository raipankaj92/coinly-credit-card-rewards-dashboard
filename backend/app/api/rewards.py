"""Reward catalogue and redemption endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.reward import RedemptionResponse, RewardResponse
from app.services.reward_service import (
    InsufficientBalanceError,
    RewardNotFoundError,
    RewardService,
    WalletNotFoundError,
)

router = APIRouter(prefix="/api/rewards", tags=["rewards"])


@router.get("", response_model=list[RewardResponse])
def list_rewards(session: Session = Depends(get_db)) -> list[RewardResponse]:
    return [RewardResponse.model_validate(reward) for reward in RewardService.list_active_rewards(session)]


@router.post("/{reward_id}/redeem", response_model=RedemptionResponse, status_code=status.HTTP_201_CREATED)
def redeem_reward(reward_id: int, session: Session = Depends(get_db)) -> RedemptionResponse:
    try:
        result = RewardService.redeem_reward(session, reward_id)
    except RewardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except WalletNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InsufficientBalanceError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return RedemptionResponse(
        redemption_id=result.redemption.id,
        reward=RewardResponse.model_validate(result.reward),
        updated_balance=result.updated_balance,
    )
