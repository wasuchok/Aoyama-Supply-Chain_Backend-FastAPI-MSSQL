from typing import Optional
from pydantic import BaseModel, ConfigDict


class SpcPartMasterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    Part_No: Optional[str]
    Part_Name: Optional[str]
    Mat_Name: Optional[str]
    Diameter: Optional[str]
    M_Size: Optional[str]
    Small: Optional[str]
    Medium: Optional[str]
    Large: Optional[str]
    Surface: Optional[str]
    Production_By: Optional[str]
    Update_Date: Optional[str]
    Update_By: Optional[str]
    Update_IP: Optional[str]
mode = True