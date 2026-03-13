from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ..models.employee import Employee
from ..schemas.employee import EmployeeCreate


class EmployeeCrud:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    async def employee_create(self, department_id: int, data_create: EmployeeCreate) -> Optional[Employee]:
        
        new_employee = Employee(department_id=department_id, **data_create.model_dump())
        
        self.db.add(new_employee)
        await self.db.commit()
        await self.db.refresh(new_employee)
        return new_employee