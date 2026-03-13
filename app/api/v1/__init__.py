from fastapi import APIRouter

from .department_router import router as department_router
from .employee_router import router as employee_router


router = APIRouter(prefix="/api/v1")

router.include_router(department_router)
router.include_router(employee_router)