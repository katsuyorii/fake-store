from fastapi import Depends

from users.repositories import UsersRepository
from users.dependencies import get_users_repository

from .services import AuthService, TokenService


async def get_token_service() -> TokenService:
    return TokenService()

async def get_auth_service(users_repository: UsersRepository = Depends(get_users_repository), token_service: TokenService = Depends(get_token_service)) -> AuthService:
    return AuthService(users_repository, token_service)