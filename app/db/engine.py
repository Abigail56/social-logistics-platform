from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.core.config import get_settings


settings = get_settings()

engine_kwargs = {"echo": False}
if settings.database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine: AsyncEngine = create_async_engine(
    settings.database_url,
    **engine_kwargs,
)
