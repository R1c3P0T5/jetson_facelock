from uuid import UUID

from src.core.exceptions import PermissionDeniedError
from src.users.models import User, UserRole


def require_self_or_admin(current_user: User, user_id: UUID) -> None:
    if current_user.id != user_id and current_user.role != UserRole.ADMIN:
        raise PermissionDeniedError()
