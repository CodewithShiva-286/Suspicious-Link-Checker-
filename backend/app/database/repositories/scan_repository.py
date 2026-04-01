from typing import Any

from app.database.mongo import mongo_manager


class ScanRepository:
    collection_name = "scan_logs"

    async def ensure_indexes(self) -> None:
        collection = mongo_manager.db[self.collection_name]
        await collection.create_index("scan_id", unique=True)
        await collection.create_index([("input.domain", 1), ("meta.started_at", -1)])

    async def insert_scan(self, document: dict[str, Any]) -> str:
        collection = mongo_manager.db[self.collection_name]
        await collection.insert_one(document)
        return document["scan_id"]

    async def get_by_scan_id(self, scan_id: str) -> dict[str, Any] | None:
        collection = mongo_manager.db[self.collection_name]
        return await collection.find_one({"scan_id": scan_id}, {"_id": 0})
