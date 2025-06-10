from core.utils.passwords import verify_password

from .repositories import UsersRepository
from .models import UserModel
from .schemas import UserUpdateSchema, UserChangePasswordSchema
from .exceptions import IncorrectPassword


class UsersService:
    def __init__(self, users_repository: UsersRepository, current_user: UserModel):
        self.users_repository = users_repository
        self.current_user = current_user
    
    async def update(self, update_user_data: UserUpdateSchema) -> UserModel:
        return await self.users_repository.update(self.current_user, update_user_data.model_dump(exclude_unset=True))
    
    async def delete(self) -> None:
        await self.users_repository.delete(self.current_user)
    
    async def change_password(self, passwords_data: UserChangePasswordSchema) -> None:
        if not verify_password(passwords_data.old_password, self.current_user.password):
            raise IncorrectPassword()
        
        await self.users_repository.change_password(self.current_user, passwords_data.new_password)
