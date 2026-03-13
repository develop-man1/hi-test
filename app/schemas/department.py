from pydantic import BaseModel, Field, StringConstraints, ConfigDict
from typing import Optional, Annotated
from datetime import datetime


DepartmentName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=200)
]


class DepartmentCreate(BaseModel):
    
    name: DepartmentName
    parent_id: Optional[int] = None
    

class DepartmentUpdate(BaseModel):
    
    name: Optional[DepartmentName] = None
    parent_id: Optional[int] = None
    
    
class DepartmentResponse(BaseModel):
    
    id: int = Field(...)
    name: DepartmentName
    parent_id: Optional[int]
    created_at: datetime
    
    
    model_config = ConfigDict(from_attributes=True)