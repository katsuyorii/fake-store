from fastapi import Response, Request

from datetime import timedelta, datetime, timezone

from src.settings import jwt_settings
from users.repositories import UsersRepository
from core.utils.passwords import hashing_password, verify_password
from core.utils.exceptions import EmailAlreadyRegistered, MissingJWTToken, InvalidJWTToken
from core.utils.jwt import create_jwt_token, verify_jwt_token
from core.repositories.redis_base import RedisBaseRepository

from .schemas import UserRegistrationSchema, UserLoginSchema, AccessTokenSchema
from .exceptions import LoginOrPasswordIncorrect, AccountNotActive, AccountMissing


class TokenBlacklistService:
    def __init__(self, redis_repository: RedisBaseRepository):
        self.redis_repository = redis_repository
    
    async def add_to_blacklist(self, payload: dict, token: str) -> None:
        key = f'blacklist:{token}'

        now = int(datetime.now(timezone.utc).timestamp())
        expire_token = payload.get('exp')
        ex = expire_token - now

        await self.redis_repository.set_key(key, 'true', ex)
    
    async def is_blacklisted(self, token: str) -> bool:
        key = f'blacklist:{token}'

        return await self.redis_repository.exists_key(key)

class TokenService:
    def create_access_token(self, payload: dict) -> str:
        access_token = create_jwt_token(payload, timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return access_token
    
    def create_refresh_token(self, payload: dict) -> str:
        refresh_token = create_jwt_token(payload, timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS))
        return refresh_token
    
    def set_token_to_cookies(self, key: str, token: str, max_age: int, response: Response) -> None:
        response.set_cookie(
            key=key,
            value=token,
            httponly=True,
            secure=True,
            samesite='strict',
            max_age=max_age,
        )

class AuthService:
    def __init__(self, users_repository: UsersRepository, token_service: TokenService, token_blacklist_service: TokenBlacklistService):
        self.users_repository = users_repository
        self.token_service = token_service
        self.token_blacklist_service = token_blacklist_service

    async def registration(self, user_data: UserRegistrationSchema) -> None:
        user = await self.users_repository.get_by_email(user_data.email)

        if user is not None:
            raise EmailAlreadyRegistered()

        user_data_dict = user_data.model_dump()
        user_data_dict['password'] = hashing_password(user_data.password)

        await self.users_repository.create(user_data_dict)
    
    async def authentication(self, user_data: UserLoginSchema, response: Response) -> AccessTokenSchema:
        user = await self.users_repository.get_by_email(user_data.email)

        if not user or not verify_password(user_data.password, user.password):
            raise LoginOrPasswordIncorrect()
        
        if user.is_active: # (Заменить на "if not" после добавления подтверждения email)
            raise AccountNotActive()
        
        access_token = self.token_service.create_access_token({'sub': str(user.id), 'role': user.role})
        refresh_token = self.token_service.create_refresh_token({'sub': str(user.id)})

        self.token_service.set_token_to_cookies('access_token', access_token, jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, response)
        self.token_service.set_token_to_cookies('refresh_token', refresh_token, jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60, response)

        return AccessTokenSchema(access_token=access_token)
    
    async def logout(self, response: Response, request: Request) -> None:
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            raise MissingJWTToken()

        payload = verify_jwt_token(refresh_token)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        await self.token_blacklist_service.add_to_blacklist(payload, refresh_token)
    
    async def refresh(self, response: Response, request: Request) -> AccessTokenSchema:
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            raise MissingJWTToken()
        
        if await self.token_blacklist_service.is_blacklisted(refresh_token):
            raise InvalidJWTToken()
        
        payload = verify_jwt_token(refresh_token)
        user = await self.users_repository.get_by_id(int(payload.get('sub')))

        if not user:
            raise AccountMissing()
        
        if user.is_active: # (Заменить на "if not" после добавления подтверждения email)
            raise AccountNotActive()

        access_token = self.token_service.create_access_token({'sub': str(user.id), 'role': user.role})
        new_refresh_token = self.token_service.create_refresh_token({'sub': str(user.id)})

        self.token_service.set_token_to_cookies('access_token', access_token, jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, response)
        self.token_service.set_token_to_cookies('refresh_token', new_refresh_token, jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60, response)

        return AccessTokenSchema(access_token=access_token)