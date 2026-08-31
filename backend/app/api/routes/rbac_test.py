from fastapi import APIRouter, Depends

from app.core.permissions import require_permission
from app.models.user import User


router = APIRouter(
    prefix="/rbac-test",
    tags=["RBAC"],
)


@router.get(
    "/workflow-create",
)
def test_workflow_create_permission(
    current_user: User = Depends(
        require_permission("workflow:create")
    ),
):
    return {
        "message": "You have workflow:create permission",
        "user_id": str(current_user.id),
        "role_id": str(current_user.role_id),
    }