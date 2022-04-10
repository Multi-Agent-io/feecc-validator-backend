import os
import sys

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient


def _get_database_name() -> str:
    """Get DB name in cluster from a MongoDB connection url"""
    mongo_connection_url: str = os.getenv("MONGO_CONNECTION_URL", "")
    db_name: str = mongo_connection_url.split("/")[-1]

    if "?" in db_name:
        db_name = db_name.split("?")[0]

    return db_name


def _get_database_client() -> AsyncIOMotorClient:
    """Get MongoDB connection url"""
    mongo_connection_url: str = os.getenv("MONGO_CONNECTION_URL", "")

    try:
        db_client = AsyncIOMotorClient(mongo_connection_url, serverSelectionTimeoutMS=3000)
        db_client.server_info()
        return db_client

    except Exception as E:
        message = (
            f"Failed to establish database connection: {E}. "
            f"Is the provided URI correct? {mongo_connection_url=} Exiting."
        )
        logger.critical(message)
        sys.exit(1)
