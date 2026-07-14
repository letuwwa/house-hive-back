from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.db.deps import get_db
from app.db.models import House, User
from app.core.security import get_current_user
from app.api.v1.schemas import HouseCreate, HouseRead, HouseUpdate


router = APIRouter(prefix="/houses", tags=["houses"])


@router.post(
    "",
    response_model=HouseRead,
    status_code=status.HTTP_201_CREATED,
)
def create_house(
    house_in: HouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> House:
    house = House(
        name=house_in.name,
        address=house_in.address,
        rooms=house_in.rooms,
    )

    db.add(house)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid house data",
        ) from exc

    db.refresh(house)
    return house


@router.get("", response_model=list[HouseRead])
def list_houses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[House]:
    return list(db.scalars(select(House).order_by(House.created_at.desc())))


@router.get("/{house_id}", response_model=HouseRead)
def get_house(
    house_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> House:
    return _get_house_or_404(db, house_id)


@router.patch("/{house_id}", response_model=HouseRead)
def update_house(
    house_id: UUID,
    house_in: HouseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> House:
    house = _get_house_or_404(db, house_id)
    update_data = house_in.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(house, field, value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid house data",
        ) from exc

    db.refresh(house)
    return house


@router.delete("/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_house(
    house_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    house = _get_house_or_404(db, house_id)
    db.delete(house)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def _get_house_or_404(db: Session, house_id: UUID) -> House:
    house = db.get(House, house_id)
    if house is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="House not found",
        )
    return house
