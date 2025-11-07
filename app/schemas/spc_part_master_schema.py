from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class SpcPartMasterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    Part_No: Optional[str] = None
    Part_Name: Optional[str] = None
    Mat_Name: Optional[str] = None
    Diameter: Optional[str] = None
    M_Size: Optional[str] = None
    Small: Optional[str] = None
    Medium: Optional[str] = None
    Large: Optional[str] = None
    Surface: Optional[str] = None
    Production_By: Optional[str] = None
    Update_Date: Optional[str] = None
    Update_By: Optional[str] = None
    Update_IP: Optional[str] = None


class PartInformationResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    Part_No: Optional[str] = None
    Tier_No: Optional[int] = None
    Sup_Code: Optional[str] = None
    Sup_Name: Optional[str] = None
    Inductrial_Estate: Optional[str] = None
    Address: Optional[str] = None
    Country: Optional[str] = None
    Province: Optional[str] = None
    District: Optional[str] = None
    Chain_Process: Optional[str] = None
    C_mat_name: Optional[str] = None
    c_diameter: Optional[str] = None
    Std_Stock: Optional[int] = None
    Dual_Source: Optional[str] = None
    d_sup_name: Optional[str] = None
    d_Inductrial_Estate: Optional[str] = None
    d_address: Optional[str] = None
    d_country: Optional[str] = None
    d_province: Optional[str] = None
    d_district: Optional[str] = None
    PD_Replacement: Optional[str] = None
    p_sup_name: Optional[str] = None
    p_Inductrial_Estate: Optional[str] = None
    p_address: Optional[str] = None
    p_country: Optional[str] = None
    p_province: Optional[str] = None
    p_district: Optional[str] = None


class SpcPartMasterDetailResponse(BaseModel):
    PartMaster: Optional[SpcPartMasterResponse] = None
    PartInformation: List[PartInformationResponse] = Field(default_factory=list)
