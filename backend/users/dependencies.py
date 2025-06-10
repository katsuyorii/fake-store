from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.database import get_db
from core.utils.jwt import verify_jwt_token

from .models import UserModel
from .services import UsersService
from .repositories import UsersRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_users_repository(db: AsyncSession = Depends(get_db)) -> UsersRepository:
    return UsersRepository(db)

async def get_current_user(token: str = Depends(oauth2_scheme), users_repository: UsersRepository = Depends(get_users_repository)) -> UserModel:
    payload = verify_jwt_token(token)
    user_id = int(payload.get('sub'))

    user = await users_repository.get_by_id(user_id)

    return user

async def get_users_service(users_repository: UsersRepository = Depends(get_users_repository), current_user: UserModel = Depends(get_current_user)) -> UsersService:
    return UsersService(users_repository, current_user)