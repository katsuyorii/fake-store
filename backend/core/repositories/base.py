from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, model, db: AsyncSession):
        self.model = model
        self.db = db
    
    async def get_all(self):
        result = await self.db.execute(select(self.model))
        return result.scalars().all()
    
    async def get_by_id(self, id: int):
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
    
    async def create(self, obj_data: dict):
        obj = self.model(**obj_data)
        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
    
    async def update(self, obj, obj_data: dict):
        for key, value in obj_data.items():
            setattr(obj, key, value)
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
    
    async def delete(self, obj):
        await self.db.delete(obj)
        await self.db.commit()