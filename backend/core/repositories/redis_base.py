from redis.asyncio import Redis


class RedisBaseRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_key(self, key: str, value: str, ex: int | None = None) -> None:
        self.redis.set(key, value, ex)
    
    async def get_key(self, key: str) -> str | None:
        return self.redis.get(key)
    
    async def delete_key(self, key: str) -> None:
        self.redis.delete(key)

    async def exists_key(self, key: str) -> bool:
        return self.redis.exists(key) > 0