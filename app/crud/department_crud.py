from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import Optional

from ..models.employee import Employee
from ..models.department import Department
from ..schemas.department import DepartmentCreate, DepartmentUpdate


class DepartmentCrud:
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    
    async def get_department(self, id: int) -> Optional[Department]:
        stmt = select(Department).where(Department.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        
        
    async def get_children(self, parent_id: int) -> list[Department]:
        stmt = select(Department).where(Department.parent_id == parent_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    
    async def get_employees(self, department_id: int) -> list:
        stmt = select(Employee).where(Employee.department_id == department_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    
    async def reassign_employees(self, from_id: int, to_id: int) -> None:
        stmt = update(Employee).where(Employee.department_id == from_id).values(department_id=to_id)
        await self.db.execute(stmt)
        await self.db.commit()
    
    
    async def department_create(self, data_create: DepartmentCreate) -> Optional[Department]:
        
        new_department = Department(**data_create.model_dump())
        
        self.db.add(new_department)
        await self.db.commit()
        await self.db.refresh(new_department)
        return new_department
    
    
    async def department_update(self, id: int, data_update: DepartmentUpdate) -> Optional[Department]:
        
        stmt = update(Department).where(Department.id == id).values(**data_update.model_dump(exclude_none=True)).returning(Department)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()
    
    
    async def department_delete(self, id: int) -> Optional[Department]:
        
        stmt = delete(Department).where(Department.id == id).returning(Department)
        result = await self.db.execute(stmt)
        
        await self.db.commit()
        return result.scalar_one_or_none()