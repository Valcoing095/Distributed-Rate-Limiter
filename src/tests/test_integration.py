import asyncio
import os

import pytest
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from rate_limiter.models import Base, RateLimitAuditLog, RateLimitPolicy
from rate_limiter.postgres_repository import PostgresRateLimiterRepository
from rate_limiter.repository import RedisRateLimiterRepository
from rate_limiter.service import RateLimiterService

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def redis_client():
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 6379))
    client = Redis(host=host, port=port, decode_responses=True)
    yield client
    await client.flushdb()
    await client.aclose()


@pytest.fixture
async def db_session():
    database_url = os.getenv(
        "DATABASE_URL",

        "postgresql+asyncpg://test_user:test_password@postgres-test:5432/rate_limiter_test_db",
    )
    engine = create_async_engine(database_url, echo=False)

    session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with session_factory() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


async def test_orchestrator_full_flow(redis_client, db_session):

    redis_repo = RedisRateLimiterRepository(redis_client)
    postgres_repo = PostgresRateLimiterRepository(db_session)
    service = RateLimiterService(redis_repo, postgres_repo)

    user_id = "user_premium_99"
    endpoint = "/api/v1/solicitar-prestamo"

    allowed, remaining = await service.process_request(
        user_identifier=user_id,
        endpoint_path=endpoint,
        default_max_requests=1,
        default_window_seconds=2,
    )
    assert allowed is True
    assert remaining == 0

    allowed, _ = await service.process_request(
        user_id, endpoint, default_max_requests=1, default_window_seconds=2
    )
    assert allowed is False

    nueva_politica = RateLimitPolicy(
        name="Límite Préstamos",
        endpoint_path=endpoint,
        max_requests=3,
        window_seconds=10,
    )
    db_session.add(nueva_politica)
    await db_session.commit()

    await redis_client.flushdb()

    p1_ok, r1 = await service.process_request(user_id, endpoint, default_max_requests=1)
    p2_ok, r2 = await service.process_request(user_id, endpoint, default_max_requests=1)
    p3_ok, r3 = await service.process_request(user_id, endpoint, default_max_requests=1)
    p4_blocked, r4 = await service.process_request(
        user_id, endpoint, default_max_requests=1
    )

    assert p1_ok is True and r1 == 2
    assert p2_ok is True and r2 == 1
    assert p3_ok is True and r3 == 0
    assert p4_blocked is False

    from sqlalchemy import select

    query = select(RateLimitAuditLog).where(
        RateLimitAuditLog.user_identifier == user_id
    )
    result = await db_session.execute(query)
    logs = result.scalars().all()

    assert len(logs) == 6

    assert logs[-1].is_allowed is False
