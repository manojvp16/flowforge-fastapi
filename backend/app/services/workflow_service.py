from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.repositories.workflow_repository import (
    WorkflowRepository,
)
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
)


def serialize_workflow(document: dict) -> dict:
    document["id"] = str(
        document.pop("_id")
    )

    return document


def create_workflow(
    repository: WorkflowRepository,
    request: WorkflowCreate,
    organization_id: str,
    user_id: str,
) -> dict:

    now = datetime.now(timezone.utc)

    document = {
        "organization_id": organization_id,
        "created_by": user_id,

        "name": request.name,
        "description": request.description,
        "status": request.status,

        "trigger": request.trigger.model_dump(),
        "steps": [
            step.model_dump()
            for step in request.steps
        ],

        "created_at": now,
        "updated_at": now,
    }

    workflow = repository.create(
        document
    )

    return serialize_workflow(workflow)


def get_workflows(
    repository: WorkflowRepository,
    organization_id: str,
) -> list[dict]:

    workflows = repository.find_all(
        organization_id
    )

    return [
        serialize_workflow(workflow)
        for workflow in workflows
    ]


def get_workflow(
    repository: WorkflowRepository,
    workflow_id: str,
    organization_id: str,
) -> dict:

    workflow = repository.find_by_id(
        workflow_id,
        organization_id,
    )

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found",
        )

    return serialize_workflow(workflow)


def update_workflow(
    repository: WorkflowRepository,
    workflow_id: str,
    organization_id: str,
    request: WorkflowUpdate,
) -> dict:

    updates = request.model_dump(
        exclude_unset=True
    )

    if "trigger" in updates:
        updates["trigger"] = (
            request.trigger.model_dump()
            if request.trigger
            else None
        )

    if "steps" in updates and request.steps:
        updates["steps"] = [
            step.model_dump()
            for step in request.steps
        ]

    workflow = repository.update(
        workflow_id,
        organization_id,
        updates,
    )

    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found",
        )

    return serialize_workflow(workflow)


def delete_workflow(
    repository: WorkflowRepository,
    workflow_id: str,
    organization_id: str,
) -> None:

    deleted = repository.delete(
        workflow_id,
        organization_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found",
        )