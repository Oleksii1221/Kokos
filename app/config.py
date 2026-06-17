from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    bot_token: str = Field(alias="BOT_TOKEN")
    owner_id: int = Field(default=0, alias="OWNER_ID")
    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    bot_maintenance: bool = Field(default=False, alias="BOT_MAINTENANCE")
    max_parallel_downloads: int = Field(default=3, alias="MAX_PARALLEL_DOWNLOADS")
    max_video_mb: int = Field(default=48, alias="MAX_VIDEO_MB")
    download_timeout_seconds: int = Field(default=120, alias="DOWNLOAD_TIMEOUT_SECONDS")
    public_stats: bool = Field(default=True, alias="PUBLIC_STATS")


@lru_cache
def get_settings() -> Settings:
    return Settings()

