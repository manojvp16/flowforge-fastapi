def workflow_payload():
    return {
        "name": "Test Leave Workflow",
        "description": "Workflow created during testing",
        "status": "draft",
        "trigger": {
            "type": "manual",
            "config": {},
        },
        "steps": [
            {
                "type": "notification",
                "name": "Notify Employee",
                "config": {
                    "channel": "email",
                },
            }
        ],
    }


def test_create_workflow(client):

    response = client.post(
        "/workflows",
        json=workflow_payload(),
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Leave Workflow"
    assert data["description"] == "Workflow created during testing"
    assert data["status"] == "draft"
    assert "id" in data


def test_list_workflows(client):

    client.post(
        "/workflows",
        json=workflow_payload(),
    )

    response = client.get(
        "/workflows"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Test Leave Workflow"


def test_get_workflow(client):

    create_response = client.post(
        "/workflows",
        json=workflow_payload(),
    )

    assert create_response.status_code == 201

    workflow_id = create_response.json()["id"]

    response = client.get(
        f"/workflows/{workflow_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == workflow_id
    assert data["name"] == "Test Leave Workflow"


def test_update_workflow(client):

    create_response = client.post(
        "/workflows",
        json=workflow_payload(),
    )

    assert create_response.status_code == 201

    workflow_id = create_response.json()["id"]

    response = client.put(
        f"/workflows/{workflow_id}",
        json={
            "name": "Updated Workflow",
            "status": "active",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == workflow_id
    assert data["name"] == "Updated Workflow"
    assert data["status"] == "active"


def test_delete_workflow(client):

    create_response = client.post(
        "/workflows",
        json=workflow_payload(),
    )

    assert create_response.status_code == 201

    workflow_id = create_response.json()["id"]

    response = client.delete(
        f"/workflows/{workflow_id}"
    )

    assert response.status_code == 204

    get_response = client.get(
        f"/workflows/{workflow_id}"
    )

    assert get_response.status_code == 404


def test_execution_history(client):

    create_response = client.post(
        "/workflows",
        json={
            "name": "Execution History Test",
            "description": "Testing execution history",
            "status": "active",
            "trigger": {
                "type": "manual",
                "config": {},
            },
            "steps": [
                {
                    "type": "notification",
                    "name": "Notify",
                    "config": {
                        "channel": "email",
                    },
                }
            ],
        },
    )

    assert create_response.status_code == 201

    workflow_id = create_response.json()["id"]

    execute_response = client.post(
        f"/workflows/{workflow_id}/execute",
        json={
            "input": {
                "employee_id": "EMP-TEST",
            }
        },
    )

    assert execute_response.status_code == 200

    execution = execute_response.json()

    assert execution["workflow_id"] == workflow_id
    assert execution["status"] == "completed"

    history_response = client.get(
        f"/workflows/{workflow_id}/executions"
    )

    assert history_response.status_code == 200

    history = history_response.json()

    assert history["total"] == 1
    assert len(history["items"]) == 1

    history_execution = history["items"][0]

    assert history_execution["workflow_id"] == workflow_id
    assert history_execution["status"] == "completed"