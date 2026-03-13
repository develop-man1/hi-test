from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..crud.employee_crud import EmployeeCrud
from ..crud.department_crud import DepartmentCrud
from ..schemas.employee import EmployeeResponse, EmployeeCreate


class EmployeeService:
    
    def __init__(self, db: AsyncSession):
        self.employee_crud = EmployeeCrud(db)
        self.department_crud = DepartmentCrud(db)
        
    
    async def create_employee(self, department_id: int, data: EmployeeCreate) -> EmployeeResponse:
        
        department = await self.department_crud.get_department(department_id)
        
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
            
        new_employee = await self.employee_crud.employee_create(department_id, data)
        
        return EmployeeResponse.model_validate(new_employee)