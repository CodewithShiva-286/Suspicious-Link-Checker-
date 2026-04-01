from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config.settings import Settings


class MongoManager:
    def __init__(self) -> None:
        self._client: AsyncIOMotorClient | None = None
        self._db: AsyncIOMotorDatabase | None = None

    def connect(self, settings: Settings) -> None:
        self._client = AsyncIOMotorClient(settings.MONGODB_URI)
        self._db = self._client[settings.MONGODB_DB_NAME]

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
        self._client = None
        self._db = None

    @property
    def db(self) -> AsyncIOMotorDatabase:
        if self._db is None:
            raise RuntimeError("MongoDB not connected.")
        return self._db


mongo_manager = MongoManager()
