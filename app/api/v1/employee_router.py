from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...schemas.employee import EmployeeCreate, EmployeeResponse
from ...services.employee_service import EmployeeService


router = APIRouter(prefix="/departments", tags=["Employees"])


@router.post("/{id}/employees/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(id: int, data: EmployeeCreate, db: AsyncSession = Depends(get_db)):
    
    service = EmployeeService(db)
    
    return await service.create_employee(id, data)