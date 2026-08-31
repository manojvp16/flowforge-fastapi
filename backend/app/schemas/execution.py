from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class WorkflowExecutionRequest(BaseModel):
    input: dict[str, Any] = Field(
        default_factory=dict
    )


class StepExecutionResult(BaseModel):
    step_name: str
    step_type: str
    status: Literal[
        "completed",
        "failed",
        "skipped",
    ]
    result: Any = None


class WorkflowExecutionResponse(BaseModel):
    execution_id: str
    workflow_id: str
    organization_id: str
    triggered_by: str

    status: Literal[
        "completed",
        "failed",
    ]

    input: dict[str, Any]

    steps: list[StepExecutionResult]

    started_at: datetime
    completed_at: datetime