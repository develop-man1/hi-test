from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

from ..core.database import Base


class Department(Base):
    
    __tablename__ = 'departments'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True) # я решил сделать SET NULL, чтобы дочерние таблицы после удаления родителя не удалялись через CASCADE, а просто имели у себя null
    created_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (UniqueConstraint("name", "parent_id", name="unique_parent_name"), )
    
    parent = relationship("Department", remote_side=[id], backref="children")
    employees = relationship("Employee", back_populates="department")