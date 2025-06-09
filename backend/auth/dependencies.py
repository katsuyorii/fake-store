from fastapi import Depends

from users.repositories import UsersRepository
from users.dependencies import get_users_repository

from .services import AuthService


async def get_auth_service(users_repository: UsersRepository = Depends(get_users_repository)) -> AuthService:
    return AuthService(users_repository)