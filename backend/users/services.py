from .repositories import UsersRepository
from .models import UserModel
from .schemas import UserUpdateSchema


class UsersService:
    def __init__(self, users_repository: UsersRepository, current_user: UserModel):
        self.users_repository = users_repository
        self.current_user = current_user
    
    async def update(self, update_user_data: UserUpdateSchema) -> UserModel:
        return await self.users_repository.update(self.current_user, update_user_data.model_dump(exclude_unset=True))