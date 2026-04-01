from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "Suspicious Link Checker API"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = False

    API_PREFIX: str = "/api/v1"

    GOOGLE_SAFE_BROWSING_API_KEY: str = ""
    VIRUSTOTAL_API_KEY: str = ""
    WHOIS_API_KEY: str = ""

    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "link_checker"

    REQUEST_TIMEOUT_MS: int = 8000
    MAX_URL_LENGTH: int = 2048
    ALLOWED_SCHEMES: str = "http,https"

    MAX_CONCURRENT_PROVIDER_CALLS: int = 4
    ENABLE_SCAN_PERSISTENCE: bool = True

    FRONTEND_ORIGIN: str = "http://localhost:5173"
    # Comma-separated list; when empty, only FRONTEND_ORIGIN is allowed.
    CORS_ORIGINS: str = ""
    # Optional regex for preview URLs (e.g. https://.*\.vercel\.app).
    CORS_ORIGIN_REGEX: str = ""

    PRIVATE_NETWORK_SCAN_ALLOWED: bool = False
    LOOPBACK_SCAN_ALLOWED: bool = False

    VT_MALICIOUS_OVERRIDE_THRESHOLD: int = Field(default=5, ge=1)

    @property
    def allowed_schemes_set(self) -> set[str]:
        return {item.strip().lower() for item in self.ALLOWED_SCHEMES.split(",") if item.strip()}

    @property
    def cors_allow_origins(self) -> list[str]:
        if self.CORS_ORIGINS.strip():
            return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]
        return [self.FRONTEND_ORIGIN]


@lru_cache
def get_settings() -> Settings:
    return Settings()
