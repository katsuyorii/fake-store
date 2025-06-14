from fastapi import APIRouter, Depends, status

from .services import UsersService, UsersAddressService, UsersEmailService
from .schemas import UserResponseSchema, UserUpdateSchema, UserChangePasswordSchema, UserChangeEmailSchema, UserAddressesResponseSchema, UserAddressCreateSchema, UserAddressUpdateSchema
from .dependencies import get_users_service, get_users_repository, get_users_email_service, get_users_address_service
from .repositories import UsersRepository


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

@users_router.patch('/me/password')
async def change_password_account(passwords_data: UserChangePasswordSchema, users_service: UsersService = Depends(get_users_service)):
    await users_service.change_password(passwords_data)
    return {'message': 'Password successfully changed!'}

@users_router.patch('/me/email')
async def change_email_account(email_data: UserChangeEmailSchema, users_service: UsersService = Depends(get_users_service)):
    await users_service.change_email(email_data)
    return {'message': 'Confirmation letter successfully sent to your email!'}

@users_router.get('/me/change-email')
async def verify_change_email_user(token: str, users_repository: UsersRepository = Depends(get_users_repository), users_email_service: UsersEmailService = Depends(get_users_email_service)):
    users_service = UsersService(users_repository, users_email_service, None)
    await users_service.verify_change_email(token)
    return {'message': 'Email address successfully changed!'}

@users_router.get('/me/addresses', response_model=list[UserAddressesResponseSchema])
async def get_addresses(users_address_service: UsersAddressService = Depends(get_users_address_service)):
    return await users_address_service.get_addresses()

@users_router.get('/me/addresses/{address_id}', response_model=UserAddressesResponseSchema)
async def get_address(address_id: int, users_address_service: UsersAddressService = Depends(get_users_address_service)):
    return await users_address_service.get_address(address_id)

@users_router.post('/me/addresses', response_model=UserAddressesResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_address(address_data: UserAddressCreateSchema, users_address_service: UsersAddressService = Depends(get_users_address_service)):
    return await users_address_service.create_address(address_data)

@users_router.delete('/me/addresses/{address_id}')
async def delete_address(address_id: int, users_address_service: UsersAddressService = Depends(get_users_address_service)):
    await users_address_service.delete_address(address_id)
    return {'message': 'Address successfully deleted!'}

@users_router.patch('/me/addresses/{address_id}', response_model=UserAddressesResponseSchema)
async def update_address(address_id: int, updated_address_data: UserAddressUpdateSchema, users_address_service: UsersAddressService = Depends(get_users_address_service)):
    return await users_address_service.update_address(address_id, updated_address_data)