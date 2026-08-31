import os
from pathlib import Path
from uuid import UUID

from dotenv import load_dotenv

# Load test configuration BEFORE importing the application.
BASE_DIR = Path(__file__).resolve().parents[1]

load_dotenv(
    BASE_DIR / ".env.test",
    override=True,
)

from app.api.deps import get_current_user
from app.db.mongodb import mongodb
from app.main import app

import pytest
from fastapi.testclient import TestClient


TEST_DATABASE = "flowforge_test"

TEST_USER_ID = UUID(
    "ff84c883-6dfa-4560-91d3-872ccc26374f"
)

TEST_ORGANIZATION_ID = UUID(
    "6c460824-1e44-45a1-b99d-d0e8dfe60be6"
)

TEST_ROLE_ID = UUID(
    "ee153c09-3f79-4f85-affc-5abf753c623e"
)


class TestUser:
    id = TEST_USER_ID
    organization_id = TEST_ORGANIZATION_ID
    role_id = TEST_ROLE_ID
    is_active = True


@pytest.fixture
def client():

    app.dependency_overrides[
        get_current_user
    ] = lambda: TestUser()

    with TestClient(app) as test_client:

        mongodb.database = mongodb.client[
            TEST_DATABASE
        ]

        mongodb.database["workflows"].delete_many({})

        yield test_client

        mongodb.database["workflows"].delete_many({})

    app.dependency_overrides.clear()