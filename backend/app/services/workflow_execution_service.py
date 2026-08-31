from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status

from app.engine.workflow_engine import WorkflowEngine
from app.repositories.execution_repository import (
    ExecutionRepository,
)
from app.repositories.workflow_repository import (
    WorkflowRepository,
)


def execute_workflow(
    workflow_repository: WorkflowRepository,
    execution_repository: ExecutionRepository,
    engine: WorkflowEngine,
    workflow_id: str,
    organization_id: str,
    user_id: str,
    input_data: dict,
) -> dict:

    workflow = workflow_repository.find_by_id(
        workflow_id,
        organization_id,
    )

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found",
        )

    if workflow["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workflow is not active",
        )

    started_at = datetime.now(
        timezone.utc
    )

    execution_id = str(uuid4())

    execution_status, step_results = (
        engine.execute(
            workflow["steps"],
            input_data,
        )
    )

    completed_at = datetime.now(
        timezone.utc
    )

    document = {
        "execution_id": execution_id,
        "workflow_id": workflow_id,
        "organization_id": organization_id,
        "triggered_by": user_id,

        "status": execution_status,

        "input": input_data,

        "steps": step_results,

        "started_at": started_at,
        "completed_at": completed_at,
    }

    execution_repository.create(
        document
    )

    return document