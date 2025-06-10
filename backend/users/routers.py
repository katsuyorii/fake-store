from fastapi import APIRouter, Depends

from .services import UsersService
from .schemas import UserResponseSchema
from .dependencies import get_users_service


users_router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@users_router.get('/me', response_model=UserResponseSchema)
async def get_user_me(users_service: UsersService = Depends(get_users_service)):
    return users_service.current_user