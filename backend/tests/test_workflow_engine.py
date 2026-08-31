from app.engine.workflow_engine import WorkflowEngine


def test_condition_true():

    engine = WorkflowEngine()

    steps = [
        {
            "type": "condition",
            "name": "Check Leave",
            "config": {
                "field": "leave_days",
                "operator": ">",
                "value": 3,
            },
        }
    ]

    status, results = engine.execute(
        steps,
        {"leave_days": 5},
    )

    assert status == "completed"
    assert len(results) == 1
    assert results[0]["result"] is True
    assert results[0]["status"] == "completed"


def test_condition_false():

    engine = WorkflowEngine()

    steps = [
        {
            "type": "condition",
            "name": "Check Leave",
            "config": {
                "field": "leave_days",
                "operator": ">",
                "value": 3,
            },
        },
        {
            "type": "notification",
            "name": "Notify",
            "config": {
                "channel": "email",
            },
        },
    ]

    status, results = engine.execute(
        steps,
        {"leave_days": 2},
    )

    assert status == "completed"
    assert len(results) == 1
    assert results[0]["result"] is False
    assert results[0]["status"] == "skipped"


def test_notification():

    engine = WorkflowEngine()

    steps = [
        {
            "type": "notification",
            "name": "Send Email",
            "config": {
                "channel": "email",
            },
        }
    ]

    status, results = engine.execute(
        steps,
        {},
    )

    assert status == "completed"
    assert results[0]["status"] == "completed"
    assert results[0]["result"]["sent"] is True
    assert results[0]["result"]["channel"] == "email"


def test_approval():

    engine = WorkflowEngine()

    steps = [
        {
            "type": "approval",
            "name": "Manager Approval",
            "config": {
                "approver_role": "MANAGER",
            },
        }
    ]

    status, results = engine.execute(
        steps,
        {},
    )

    assert status == "completed"
    assert results[0]["status"] == "completed"
    assert results[0]["result"] is True


def test_unsupported_step():

    engine = WorkflowEngine()

    steps = [
        {
            "type": "unknown",
            "name": "Unknown Step",
            "config": {},
        }
    ]

    status, results = engine.execute(
        steps,
        {},
    )

    assert status == "failed"
    assert results[0]["status"] == "failed"
    assert "Unsupported step type" in results[0]["result"]