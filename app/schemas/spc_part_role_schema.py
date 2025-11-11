from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SpcPartRoleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    emp_no: str = Field(..., max_length=50, description="Employee identifier")
    role: str = Field(..., max_length=50, description="Role name within SPC part module")
    password: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Plain password; service will hash before storage",
    )


class SpcPartRoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, extra="allow")

    emp_no: Optional[str] = None
    role: Optional[str] = None
