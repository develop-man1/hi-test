from pydantic import BaseModel, Field, StringConstraints, ConfigDict
from typing import Optional, Annotated
from datetime import date, datetime


LimitAnnotated = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
]


class EmployeeCreate(BaseModel):
    
    full_name: LimitAnnotated
    position: LimitAnnotated
    hired_at: Optional[date] = None
    

class EmployeeResponse(BaseModel):
    
    id: int = Field(...)
    department_id: Optional[int]
    full_name: LimitAnnotated
    position: LimitAnnotated
    hired_at: Optional[date] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)