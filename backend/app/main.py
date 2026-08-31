from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models

from app.api.routes.auth import router as auth_router
from app.api.routes.rbac_test import router as rbac_test_router
from app.api.routes.workflows import router as workflow_router

from app.core.config import settings

from app.db.mongodb import (
    close_mongodb_connection,
    connect_to_mongodb,
    mongodb,
)

from app.db.postgres import check_postgres_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongodb()

    print("Application started")

    yield

    close_mongodb_connection()

    print("Application stopped")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Configurable Workflow & Integration Platform",
    lifespan=lifespan,
)


app.include_router(auth_router)
app.include_router(rbac_test_router)
app.include_router(workflow_router)


@app.get("/health")
async def health_check():

    mongodb_status = (
        "connected"
        if mongodb.client
        else "disconnected"
    )

    postgres_status = (
        "connected"
        if check_postgres_connection()
        else "disconnected"
    )

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "databases": {
            "mongodb": mongodb_status,
            "postgresql": postgres_status,
        },
    }