from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status

from app.db.deps import get_db
from app.db.models import Settlement, User
from app.core.security import get_current_user
from app.api.v1.schemas import SettlementCreate, SettlementRead
from app.api.v1.utils import require_house_member, require_house_member_id


router = APIRouter(prefix="/houses/{house_id}/settlements", tags=["settlements"])


@router.post(
    "",
    response_model=SettlementRead,
    status_code=status.HTTP_201_CREATED,
)
def create_settlement(
    house_id: UUID,
    settlement_in: SettlementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Settlement:
    require_house_member(db, house_id, current_user.id)
    require_house_member_id(db, house_id, settlement_in.from_member_id)
    require_house_member_id(db, house_id, settlement_in.to_member_id)

    if settlement_in.from_member_id == settlement_in.to_member_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Settlement members must be different",
        )

    settlement = Settlement(
        house_id=house_id,
        from_member_id=settlement_in.from_member_id,
        to_member_id=settlement_in.to_member_id,
        amount_cents=settlement_in.amount_cents,
        note=settlement_in.note,
    )
    if settlement_in.settled_at is not None:
        settlement.settled_at = settlement_in.settled_at

    db.add(settlement)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid settlement data",
        ) from exc

    db.refresh(settlement)
    return settlement


@router.get("", response_model=list[SettlementRead])
def list_settlements(
    house_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Settlement]:
    require_house_member(db, house_id, current_user.id)
    return list(
        db.scalars(
            select(Settlement)
            .where(Settlement.house_id == house_id)
            .order_by(Settlement.settled_at.desc(), Settlement.created_at.desc())
        )
    )
