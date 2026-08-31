# FlowForge

FlowForge is a configurable workflow and integration platform built as a portfolio project for demonstrating Python, FastAPI, MongoDB, PostgreSQL, testing, API design, RBAC, workflow execution, integrations, CI/CD, and cloud deployment.

## Current milestone

- FastAPI application
- Health endpoint
- MongoDB connection
- PostgreSQL connection check
- SQLAlchemy foundation
- Initial Organization model
- pytest setup
- Docker Compose infrastructure

## Project roadmap

1. Project foundation
2. Database architecture
3. Organization, users, roles, permissions
4. JWT authentication and RBAC
5. Workflow modelling and CRUD
6. Workflow execution engine
7. Conditions and approvals
8. Workflow versioning
9. Webhook integrations and retries
10. Audit logging and structured logging
11. Unit/integration/API tests
12. API regression framework
13. Docker and CI/CD
14. Locust performance testing
15. AWS deployment
16. React workflow builder and analytics dashboard

## Run locally

### Prerequisites

- Python 3.11+
- Docker Desktop
- Git

### Backend setup

```powershell
cd backend
python -m venv venv
.env\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

### Start databases

From the project root:

```powershell
docker compose up -d
docker compose ps
```

### Start API

```powershell
cd backend
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

### Run tests

```powershell
pytest
```

## Important

`.env` is ignored by Git. Never commit real secrets, passwords, API keys, or tokens.

For the current local Docker setup, the PostgreSQL development credentials are defined in `docker-compose.yml`. Change them before using the project outside local development.
