from fastapi import HTTPException, status


class EmailAlreadyRegistered(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail='Email is already registered')

class MissingJWTToken(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing JWT token')

class InvalidJWTToken(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')