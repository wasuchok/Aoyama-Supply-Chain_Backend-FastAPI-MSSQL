from sqlalchemy import Column, String
from app.core.database import Base

class SpcPartMasterModel(Base):
    __tablename__ = "Tb_Spc_Part_Master"

    Part_No = Column(String(20), primary_key=True, index=True)
    Part_Name = Column(String(50), nullable=True)
    Mat_Name = Column(String(50), nullable=True)
    Diameter = Column(String(10), nullable=True)
    M_Size = Column(String(10), nullable=True)
    Small = Column(String(50), nullable=True)
    Medium = Column(String(50), nullable=True)
    Large = Column(String(50), nullable=True)
    Surface = Column(String(50), nullable=True)
    Production_By = Column(String(20), nullable=True)
    Update_Date = Column(String(14), nullable=True)
    Update_By = Column(String(10), nullable=True)
    Update_IP = Column(String(20), nullable=True)