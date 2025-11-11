from sqlalchemy import Column, String
from app.core.database import Base


class SpcPartRoleModel(Base):
    __tablename__ = "Tb_Spc_Part_Role"

    emp_no = Column(String(50), primary_key=True, nullable=False)
    role = Column(String(50), nullable=True)
    password = Column(String(64), nullable=True)
