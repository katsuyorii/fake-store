from datetime import timedelta

from core.utils.passwords import verify_password
from core.utils.jwt import create_jwt_token
from core.services.email_service import EmailService
from core.utils.exceptions import EmailAlreadyRegistered
from core.tasks import send_email_task
from src.settings import smtp_settings, path_settings

from .repositories import UsersRepository
from .models import UserModel
from .schemas import UserUpdateSchema, UserChangePasswordSchema, UserChangeEmailSchema
from .exceptions import IncorrectPassword


class UsersEmailService(EmailService):
    def create_change_email_message(self, user_id: int) -> str:
        verify_token = create_jwt_token({'sub': str(user_id)}, timedelta(minutes=smtp_settings.EMAIL_MESSAGE_EXPIRE_MINUTES))
        message = self.render_email_template(verify_token, 'verify_email.html', path_settings.EMAIL_CHANGE_PATH)
    
        return message

class UsersService:
    def __init__(self, users_repository: UsersRepository, current_user: UserModel, users_email_service: UsersEmailService):
        self.users_repository = users_repository
        self.users_email_service = users_email_service
        self.current_user = current_user
    
    async def update(self, update_user_data: UserUpdateSchema) -> UserModel:
        return await self.users_repository.update(self.current_user, update_user_data.model_dump(exclude_unset=True))
    
    async def delete(self) -> None:
        await self.users_repository.delete(self.current_user)
    
    async def change_password(self, passwords_data: UserChangePasswordSchema) -> None:
        if not verify_password(passwords_data.old_password, self.current_user.password):
            raise IncorrectPassword()
        
        await self.users_repository.change_password(self.current_user, passwords_data.new_password)
    
    async def change_email(self, email_data: UserChangeEmailSchema) -> None:
        user = await self.users_repository.get_by_email(email_data.new_email)

        if user is not None:
            raise EmailAlreadyRegistered()
        
        message = self.users_email_service.create_change_email_message(self.current_user.id)
        send_email_task.delay(email_data.new_email, 'Смена адреса электронной почты', message)
