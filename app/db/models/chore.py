import enum
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    Text,
    Enum,
    Uuid,
    String,
    ForeignKey,
    UniqueConstraint,
    ForeignKeyConstraint,
)

from app.db.models.base_model import BaseModel


class ChoreStatus(str, enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Chore(BaseModel):
    __tablename__ = "chores"
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "house_id"],
            ["house_members.user_id", "house_members.house_id"],
            name="fk_chores_user_house_member",
        ),
        UniqueConstraint("id", "house_id", name="uq_chores_id_house"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("users.id"),
        nullable=False,
    )
    house_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("houses.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    status: Mapped[ChoreStatus] = mapped_column(
        Enum(ChoreStatus, name="chore_status"),
        default=ChoreStatus.ACTIVE,
        nullable=False,
    )
