from fastapi import APIRouter, status, Depends, Response, Request

from .schemas import UserRegistrationSchema, UserLoginSchema, AccessTokenSchema
from .services import AuthService
from .dependencies import get_auth_service


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@auth_router.post('/registration', status_code=status.HTTP_201_CREATED)
async def registration_user(user_data: UserRegistrationSchema, auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.registration(user_data)
    return {'message': 'Confirmation letter successfully sent to your email!'}

@auth_router.post('/login', response_model=AccessTokenSchema)
async def authentication_user(user_data: UserLoginSchema, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.authentication(user_data, response)

@auth_router.post('/logout')
async def logout_user(response: Response, request: Request, auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.logout(response, request)
    return {'message': 'Logged out successfully!'}

@auth_router.post('/refresh', response_model=AccessTokenSchema)
async def refresh_token(response: Response, request: Request, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.refresh(response, request)