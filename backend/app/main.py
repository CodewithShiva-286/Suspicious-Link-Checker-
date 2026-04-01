from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.scan import router as scan_router
from app.config.settings import get_settings
from app.database.mongo import mongo_manager
from app.database.repositories.scan_repository import ScanRepository

settings = get_settings()
repo = ScanRepository()


@asynccontextmanager
async def lifespan(_: FastAPI):
    mongo_manager.connect(settings)
    await repo.ensure_indexes()
    yield
    mongo_manager.close()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX or None,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(scan_router, prefix=settings.API_PREFIX)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
