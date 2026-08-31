from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class WorkflowTrigger(BaseModel):
    type: str = Field(
        min_length=1,
        max_length=50,
    )

    config: dict[str, Any] = Field(
        default_factory=dict
    )


class WorkflowStep(BaseModel):
    type: str = Field(
        min_length=1,
        max_length=50,
    )

    name: str | None = None

    config: dict[str, Any] = Field(
        default_factory=dict
    )


class WorkflowCreate(BaseModel):
    name: str = Field(
        min_length=3,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    status: Literal[
        "draft",
        "active",
        "inactive",
    ] = "draft"

    trigger: WorkflowTrigger

    steps: list[WorkflowStep] = Field(
        min_length=1,
        max_length=50,
    )


class WorkflowUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    status: Literal[
        "draft",
        "active",
        "inactive",
    ] | None = None

    trigger: WorkflowTrigger | None = None

    steps: list[WorkflowStep] | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )


class WorkflowResponse(BaseModel):
    id: str
    organization_id: str
    created_by: str

    name: str
    description: str | None
    status: str

    trigger: WorkflowTrigger
    steps: list[WorkflowStep]

    created_at: datetime
    updated_at: datetime