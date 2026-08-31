from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.main import app
from app.db.mongodb import mongodb
from app.db.postgres import SessionLocal
from app.api.deps import get_current_user
from app.models.role import Role


TEST_DATABASE = "flowforge_test"

TEST_USER_ID = UUID(
    "ff84c883-6dfa-4560-91d3-872ccc26374f"
)

TEST_ORGANIZATION_ID = UUID(
    "6c460824-1e44-45a1-b99d-d0e8dfe60be6"
)


class TestUser:
    id = TEST_USER_ID
    organization_id = TEST_ORGANIZATION_ID
    is_active = True


@pytest.fixture
def client():

    db = SessionLocal()

    admin_role = db.scalar(
        select(Role).where(
            Role.name == "ADMIN"
        )
    )

    if not admin_role:
        db.close()
        raise RuntimeError(
            "ADMIN role not found. "
            "Run the RBAC seed before tests."
        )

    TestUser.role_id = admin_role.id

    db.close()

    app.dependency_overrides[
        get_current_user
    ] = lambda: TestUser()

    with TestClient(app) as test_client:

        mongodb.database = mongodb.client[
            TEST_DATABASE
        ]

        mongodb.database["workflows"].delete_many({})
        mongodb.database["executions"].delete_many({})

        yield test_client

        mongodb.database["workflows"].delete_many({})
        mongodb.database["executions"].delete_many({})

    app.dependency_overrides.clear()