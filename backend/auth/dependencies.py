from fastapi import Depends

from users.repositories import UsersRepository
from users.dependencies import get_users_repository
from core.repositories.redis_base import RedisBaseRepository
from core.dependencies.redis import get_redis_repository

from .services import AuthService, TokenService, TokenBlacklistService


async def get_token_blacklist_service(redis_repository: RedisBaseRepository = Depends(get_redis_repository)) -> TokenBlacklistService:
    return TokenBlacklistService(redis_repository)

async def get_token_service() -> TokenService:
    return TokenService()

async def get_auth_service(users_repository: UsersRepository = Depends(get_users_repository), token_service: TokenService = Depends(get_token_service), token_blacklist_service: TokenBlacklistService = Depends(get_token_blacklist_service)) -> AuthService:
    return AuthService(users_repository, token_service, token_blacklist_service)