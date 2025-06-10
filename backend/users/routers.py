from fastapi import APIRouter, Depends

from .services import UsersService
from .schemas import UserResponseSchema, UserUpdateSchema
from .dependencies import get_users_service


users_router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@users_router.get('/me', response_model=UserResponseSchema)
async def get_user_me(users_service: UsersService = Depends(get_users_service)):
    return users_service.current_user

@users_router.patch('/me', response_model=UserResponseSchema)
async def update_account(update_user_data: UserUpdateSchema, users_service: UsersService = Depends(get_users_service)):
    return await users_service.update(update_user_data)

@users_router.delete('/me')
async def delete_account(users_service: UsersService = Depends(get_users_service)):
    await users_service.delete()
    return {'message': 'Account successfully deleted!'}