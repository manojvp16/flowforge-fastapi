from pymongo import MongoClient

from app.core.config import settings


class MongoDB:
    client: MongoClient | None = None
    database = None


mongodb = MongoDB()


def connect_to_mongodb() -> None:
    mongodb.client = MongoClient(
        settings.MONGODB_URL,
        serverSelectionTimeoutMS=5000,
    )

    mongodb.client.admin.command("ping")

    mongodb.database = mongodb.client[
        settings.MONGODB_DATABASE
    ]

    print("Connected to MongoDB")


def close_mongodb_connection() -> None:
    if mongodb.client:
        mongodb.client.close()
        mongodb.client = None
        mongodb.database = None

        print("MongoDB connection closed")


def get_mongodb():
    if mongodb.database is None:
        raise RuntimeError(
            "MongoDB is not connected"
        )

    return mongodb.database