from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database


class WorkflowRepository:

    def __init__(self, db: Database):
        self.collection = db["workflows"]

    def create(
        self,
        document: dict,
    ) -> dict:

        result = self.collection.insert_one(
            document
        )

        return self.collection.find_one(
            {"_id": result.inserted_id}
        )

    def find_by_id(
        self,
        workflow_id: str,
        organization_id: str,
    ) -> dict | None:

        if not ObjectId.is_valid(workflow_id):
            return None

        return self.collection.find_one(
            {
                "_id": ObjectId(workflow_id),
                "organization_id": organization_id,
            }
        )

    def find_all(
        self,
        organization_id: str,
    ) -> list[dict]:

        return list(
            self.collection.find(
                {
                    "organization_id": organization_id,
                }
            ).sort(
                "created_at",
                -1,
            )
        )

    def update(
        self,
        workflow_id: str,
        organization_id: str,
        updates: dict,
    ) -> dict | None:

        if not ObjectId.is_valid(workflow_id):
            return None

        updates["updated_at"] = datetime.now(
            timezone.utc
        )

        result = self.collection.update_one(
            {
                "_id": ObjectId(workflow_id),
                "organization_id": organization_id,
            },
            {
                "$set": updates
            },
        )

        if result.matched_count == 0:
            return None

        return self.find_by_id(
            workflow_id,
            organization_id,
        )

    def delete(
        self,
        workflow_id: str,
        organization_id: str,
    ) -> bool:

        if not ObjectId.is_valid(workflow_id):
            return False

        result = self.collection.delete_one(
            {
                "_id": ObjectId(workflow_id),
                "organization_id": organization_id,
            }
        )

        return result.deleted_count == 1