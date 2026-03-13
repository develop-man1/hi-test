from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ..crud.department_crud import DepartmentCrud
from ..models.department import Department
from ..schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from ..schemas.employee import EmployeeResponse


class DepartmentService:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.department_crud = DepartmentCrud(db)


    async def create_department(self, data: DepartmentCreate) -> DepartmentResponse:

        if data.parent_id is not None:
            parent = await self.department_crud.get_department(data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent department not found"
                )

        department = await self.department_crud.department_create(data)
        return DepartmentResponse.model_validate(department)


    async def update_department(self, id: int, data: DepartmentUpdate) -> DepartmentResponse:

        department = await self.department_crud.get_department(id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        if data.parent_id is not None:

            if data.parent_id == id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Department cannot be its own parent"
                )

            new_parent = await self.department_crud.get_department(data.parent_id)
            if not new_parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent department not found"
                )

            if await self._is_descendant(target_id=id, candidate_id=data.parent_id):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Cannot move department into its own subtree"
                )

        updated = await self.department_crud.department_update(id, data)
        return DepartmentResponse.model_validate(updated)


    async def delete_department(self, id: int, mode: str, reassign_to_department_id: Optional[int]) -> None:

        department = await self.department_crud.get_department(id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        if mode == "reassign":
            if reassign_to_department_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="reassign_to_department_id is required for reassign mode"
                )

            target = await self.department_crud.get_department(reassign_to_department_id)
            if not target:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Target department not found"
                )

            await self.department_crud.reassign_employees(id, reassign_to_department_id)
            await self.department_crud.department_delete(id)

        elif mode == "cascade":
            await self._cascade_delete(id)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="mode must be 'cascade' or 'reassign'"
            )


    async def get_department_tree(self, id: int, depth: int, include_employees: bool) -> dict:

        department = await self.department_crud.get_department(id)
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )

        return await self._build_tree(department, depth, include_employees)


    async def _build_tree(self, department: Department, depth: int, include_employees: bool) -> dict:

        result = DepartmentResponse.model_validate(department).model_dump()

        dept_id: int = result["id"]

        if include_employees:
            employees = await self.department_crud.get_employees(dept_id)
            result["employees"] = [EmployeeResponse.model_validate(e).model_dump() for e in employees]

        result["children"] = []

        if depth > 0:
            children = await self.department_crud.get_children(dept_id)
            for child in children:
                child_tree = await self._build_tree(child, depth - 1, include_employees)
                result["children"].append(child_tree)

        return result


    async def _is_descendant(self, target_id: int, candidate_id: int) -> bool:

        current_id = candidate_id
        while current_id is not None:
            if current_id == target_id:
                return True
            dept = await self.department_crud.get_department(current_id)
            if dept is None:
                break
            current_id = int(dept.parent_id) if dept.parent_id is not None else None
        return False


    async def _cascade_delete(self, id: int) -> None:
        children = await self.department_crud.get_children(id)
        for child in children:
            child_id: int = int(child.id) # type: ignore
            await self._cascade_delete(child_id)
        await self.department_crud.department_delete(id)