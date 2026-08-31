from pymongo.database import Database


class ExecutionRepository:

    def __init__(self, db: Database):
        self.collection = db["workflow_executions"]

    def create(self, document: dict) -> dict:

        result = self.collection.insert_one(
            document
        )

        return self.collection.find_one(
            {
                "_id": result.inserted_id
            }
        )

    def find_by_workflow(
        self,
        workflow_id: str,
        organization_id: str,
        page: int = 1,
        page_size: int = 10,
        status: str | None = None,
    ) -> tuple[list[dict], int]:

        query = {
            "workflow_id": workflow_id,
            "organization_id": organization_id,
        }

        if status:
            query["status"] = status

        total = self.collection.count_documents(query)

        skip = (page - 1) * page_size

        executions = list(
            self.collection.find(
                query,
                {
                    "_id": 0,
                },
            )
            .sort(
                "started_at",
                -1,
            )
            .skip(skip)
            .limit(page_size)
        )

        return executions, total