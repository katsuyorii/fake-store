from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.database_base import DatabaseBaseRepository
from core.utils.passwords import hashing_password

from .models import UserModel, UserAddress


class UsersAddressRepository(DatabaseBaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(UserAddress, db)
    
    async def get_all_addresses(self, user: UserModel, skip: int = 0, limit: int = 5) -> list[UserAddress]:
        result = await self.db.execute(select(UserAddress).offset(skip).limit(limit).where(UserAddress.user_id == user.id))

        return result.scalars().all()

class UsersRepository(DatabaseBaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(UserModel, db)
    
    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()
    
    async def verify_user(self, user: UserModel) -> None:
        user.is_active = True
        await self.db.commit()
    
    async def change_password(self, user: UserModel, password: str) -> None:
        user.password = hashing_password(password)
        await self.db.commit()
    
    async def change_email(self, user: UserModel, email: str) -> None:
        user.email = email
        await self.db.commit()