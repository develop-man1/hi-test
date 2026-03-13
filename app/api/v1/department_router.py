from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ...core.database import get_db
from ...schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from ...services.department_service import DepartmentService


router = APIRouter(prefix="/departments", tags=["Departments"])


@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(data: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    
    service = DepartmentService(db)
    
    return await service.create_department(data)


@router.get("/{id}")
async def get_department(id: int, depth: int = Query(default=1, ge=1, le=5), include_employees: bool = Query(default=True), db: AsyncSession = Depends(get_db)):
    
    service = DepartmentService(db)
    
    return await service.get_department_tree(id, depth, include_employees)


@router.patch("/{id}", response_model=DepartmentResponse)
async def update_department(id: int, data: DepartmentUpdate, db: AsyncSession = Depends(get_db)):
    
    service = DepartmentService(db)
    
    return await service.update_department(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(id: int, mode: str = Query(...), reassign_to_department_id: Optional[int] = Query(default=None), db: AsyncSession = Depends(get_db)):
    
    service = DepartmentService(db)
    
    await service.delete_department(id, mode, reassign_to_department_id)