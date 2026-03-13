from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship

from ..core.database import Base


class Employee(Base):
    
    __tablename__ = 'employees'
    
    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False, index=True)
    full_name = Column(String, nullable=False, index=True)
    position = Column(String, nullable=False)
    hired_at = Column(Date, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    department = relationship("Department", back_populates="employees")