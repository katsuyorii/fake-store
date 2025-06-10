from fastapi import Depends

from redis.asyncio import Redis

from src.redis import redis_client
from core.repositories.redis_base import RedisBaseRepository


async def get_redis() -> Redis:
    yield redis_client

async def get_redis_repository(redis: Redis = Depends(get_redis)) -> RedisBaseRepository:
    return RedisBaseRepository(redis)