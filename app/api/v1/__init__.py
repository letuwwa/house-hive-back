from .auth import router as auth_router
from .chore import router as chore_router
from .chore_completion import router as chore_completion_router
from .event import router as event_router
from .house import router as house_router
from .house_member import router as house_member_router

__all__ = [
    "auth_router",
    "chore_completion_router",
    "chore_router",
    "event_router",
    "house_member_router",
    "house_router",
]
