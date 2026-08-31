from fastapi import APIRouter, Depends, status, Query
from fastapi import HTTPException
from app.api.deps import (
    get_current_user,
)
from app.core.permissions import (
    require_permission,
)
from app.db.mongodb import get_mongodb
from app.models.user import User
from app.repositories.workflow_repository import (
    WorkflowRepository,
)
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowResponse,
    WorkflowUpdate,
)
from app.services.workflow_service import (
    create_workflow,
    delete_workflow,
    get_workflow,
    get_workflows,
    update_workflow,
)

from app.engine.workflow_engine import (
    WorkflowEngine,
)

from app.repositories.execution_repository import (
    ExecutionRepository,
)

from app.schemas.execution import (
    WorkflowExecutionRequest,
    WorkflowExecutionResponse,
)

from app.services.workflow_execution_service import (
    execute_workflow,
)

router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"],
)


def get_repository():
    return WorkflowRepository(
        get_mongodb()
    )

def get_execution_repository():
    return ExecutionRepository(
        get_mongodb()
    )

@router.post(
    "",
    response_model=WorkflowResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(
    request: WorkflowCreate,
    current_user: User = Depends(
        require_permission(
            "workflow:create"
        )
    ),
    repository: WorkflowRepository = Depends(
        get_repository
    ),
):
    return create_workflow(
        repository=repository,
        request=request,
        organization_id=str(
            current_user.organization_id
        ),
        user_id=str(
            current_user.id
        ),
    )


@router.get(
    "",
    response_model=list[WorkflowResponse],
)
def list_workflows(
    current_user: User = Depends(
        require_permission(
            "workflow:read"
        )
    ),
    repository: WorkflowRepository = Depends(
        get_repository
    ),
):
    return get_workflows(
        repository=repository,
        organization_id=str(
            current_user.organization_id
        ),
    )


@router.get(
    "/{workflow_id}",
    response_model=WorkflowResponse,
)
def get(
    workflow_id: str,
    current_user: User = Depends(
        require_permission(
            "workflow:read"
        )
    ),
    repository: WorkflowRepository = Depends(
        get_repository
    ),
):
    return get_workflow(
        repository=repository,
        workflow_id=workflow_id,
        organization_id=str(
            current_user.organization_id
        ),
    )


@router.put(
    "/{workflow_id}",
    response_model=WorkflowResponse,
)
def update(
    workflow_id: str,
    request: WorkflowUpdate,
    current_user: User = Depends(
        require_permission(
            "workflow:update"
        )
    ),
    repository: WorkflowRepository = Depends(
        get_repository
    ),
):
    return update_workflow(
        repository=repository,
        workflow_id=workflow_id,
        organization_id=str(
            current_user.organization_id
        ),
        request=request,
    )


@router.delete(
    "/{workflow_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    workflow_id: str,
    current_user: User = Depends(
        require_permission(
            "workflow:delete"
        )
    ),
    repository: WorkflowRepository = Depends(
        get_repository
    ),
):
    delete_workflow(
        repository=repository,
        workflow_id=workflow_id,
        organization_id=str(
            current_user.organization_id
        ),
    )

@router.post(
    "/{workflow_id}/execute",
    response_model=WorkflowExecutionResponse,
)
def execute(
    workflow_id: str,
    request: WorkflowExecutionRequest,
    current_user: User = Depends(
        require_permission(
            "workflow:execute"
        )
    ),
    workflow_repository: WorkflowRepository = Depends(
        get_repository
    ),
    execution_repository: ExecutionRepository = Depends(
        get_execution_repository
    ),
):
    engine = WorkflowEngine()

    return execute_workflow(
        workflow_repository=workflow_repository,
        execution_repository=execution_repository,
        engine=engine,
        workflow_id=workflow_id,
        organization_id=str(
            current_user.organization_id
        ),
        user_id=str(
            current_user.id
        ),
        input_data=request.input,
    )

@router.get(
    "/{workflow_id}/executions"
)
def execution_history(
    workflow_id: str,
    page: int = Query(
        1,
        ge=1,
    ),
    page_size: int = Query(
        10,
        ge=1,
        le=100,
    ),
    status: str | None = Query(
        None,
        pattern="^(completed|failed)$",
    ),
    current_user: User = Depends(
        require_permission("workflow:read")
    ),
    workflow_repository: WorkflowRepository = Depends(
        get_repository
    ),
    execution_repository: ExecutionRepository = Depends(
        get_execution_repository
    ),
):

    workflow = workflow_repository.find_by_id(
        workflow_id,
        str(current_user.organization_id),
    )

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    executions, total = (
        execution_repository.find_by_workflow(
            workflow_id=workflow_id,
            organization_id=str(
                current_user.organization_id
            ),
            page=page,
            page_size=page_size,
            status=status,
        )
    )

    return {
        "items": executions,
        "page": page,
        "page_size": page_size,
        "total": total,
        "pages": (
            (total + page_size - 1)
            // page_size
        ),
    }