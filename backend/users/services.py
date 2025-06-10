from .repositories import UsersRepository
from .models import UserModel


class UsersService:
    def __init__(self, users_repository: UsersRepository, current_user: UserModel):
        self.users_repository = users_repository
        self.current_user = current_user