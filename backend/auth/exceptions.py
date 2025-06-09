from fastapi import HTTPException, status


class LoginOrPasswordIncorrect(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail='Login or password is incorrect')

class AccountNotActive(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail='Account is not active')