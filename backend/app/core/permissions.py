from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user import User


def require_permission(permission_name: str):

    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:

        permission_exists = db.scalar(
            select(Permission.id)
            .join(
                RolePermission,
                RolePermission.permission_id == Permission.id,
            )
            .where(
                RolePermission.role_id == current_user.role_id,
                Permission.name == permission_name,
            )
        )

        if not permission_exists:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {permission_name}",
            )

        return current_user

    return permission_checker