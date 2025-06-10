from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.database_base import DatabaseBaseRepository

from .models import UserModel


class UsersRepository(DatabaseBaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(UserModel, db)
    
    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()
    
    async def verify_user(self, user: UserModel) -> None:
        user.is_active = True
        await self.db.commit()