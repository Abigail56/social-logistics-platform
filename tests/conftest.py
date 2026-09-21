import asyncio

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from app.db.session import get_session
from app.main import app
from app.models.delivery import Delivery
from app.models.user import User
from app.services.auth_service import hash_password


async def _prepare_database(database_url: str) -> None:
    engine = create_async_engine(database_url, poolclass=NullPool)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)

    async with session_factory() as session:
        session.add_all(
            [
                User(
                    id=1,
                    email="user01@example.com",
                    username="user01",
                    password_hash=hash_password("secret123"),
                ),
                Delivery(
                    id=1,
                    customer_id=1,
                    pickup_location="Lagos",
                    destination="Ibadan",
                    package_details="Books",
                    total_amount=2500,
                    status="REQUESTED",
                ),
            ]
        )
        await session.commit()

    await engine.dispose()


@pytest.fixture
def client(tmp_path):
    database_url = f"sqlite+aiosqlite:///{(tmp_path / 'test.db').as_posix()}"
    asyncio.run(_prepare_database(database_url))
    engine = create_async_engine(database_url, poolclass=NullPool)
    session_factory = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        asyncio.run(engine.dispose())
