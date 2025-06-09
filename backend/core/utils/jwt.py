import jwt

from fastapi import HTTPException, status

from datetime import datetime,  timezone, timedelta

from src.settings import jwt_settings


def create_jwt_token(payload: dict, expire_delta: timedelta) -> str:
    to_encode = payload.copy()
    iat = datetime.now(timezone.utc)
    exp = iat + expire_delta

    to_encode.update({'iat': iat, 'exp': exp})

    jwt_token = jwt.encode(to_encode, jwt_settings.SECRET_KEY, jwt_settings.ALGORITHM)

    return jwt_token

def verify_jwt_token(jwt_token: str) -> dict:
    try:
        payload = jwt.decode(jwt_token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM])
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Token expired')

    return payload