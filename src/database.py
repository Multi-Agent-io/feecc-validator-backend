import typing as tp

from loguru import logger
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from _db_utils import _get_database_client, _get_database_name
from models import Unit
from key_types import KeyTypes

Document = tp.Dict[str, tp.Any]


class UnitNotFoundError(BaseException):
    pass


class MongoDbWrapper:
    """handles interactions with MongoDB database"""

    @logger.catch
    def __init__(self) -> None:
        logger.info("Trying to connect to MongoDB")

        self._client: AsyncIOMotorClient = _get_database_client()
        db_name: str = _get_database_name()
        self._database: AsyncIOMotorDatabase = self._client[db_name]

        # collections
        self._unit_collection: AsyncIOMotorCollection = self._database["Unit-data"]

        logger.info("Successfully connected to MongoDB")

    @staticmethod
    async def _find_item(key: str, value: str, collection_: AsyncIOMotorCollection) -> tp.Optional[Document]:
        """
        finds one element in the specified collection, which has
        specified key matching specified value
        """
        return await collection_.find_one({key: value}, {"_id": 0})  # type: ignore

    @staticmethod
    async def _get_unit_from_raw_db_data(unit_dict: Document) -> Unit:
        return Unit(
            uuid=unit_dict.get("uuid"),
            internal_id=unit_dict.get("internal_id"),
            creation_time=unit_dict.get("creation_time"),
            passport_short_url=unit_dict.get("passport_short_url"),
            passport_ipfs_cid=unit_dict.get("passport_ipfs_cid"),
            serial_number=unit_dict.get("serial_number"),
            txn_hash=unit_dict.get("txn_hash"),
        )

    async def get_unit_by_key(self, key_type: KeyTypes, key_value: str) -> Unit:
        unit_dict = await self._find_item(key_type, key_value, self._unit_collection)
        if unit_dict is None:
            raise UnitNotFoundError(f"Unit with {key_type}={key_value} not found")
        return await self._get_unit_from_raw_db_data(unit_dict)
