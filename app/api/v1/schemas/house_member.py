from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.db.models import HouseMemberRole


class HouseMemberCreate(BaseModel):
    user_id: UUID
    house_id: UUID
    role: HouseMemberRole = HouseMemberRole.MEMBER


class HouseMemberUpdate(BaseModel):
    role: HouseMemberRole


class HouseMemberRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    house_id: UUID
    role: HouseMemberRole
