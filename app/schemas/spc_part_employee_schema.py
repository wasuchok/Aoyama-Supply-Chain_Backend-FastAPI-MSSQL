from typing import List, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field


class SpcPartEmployeeResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    efname: Optional[str] = None
    elname: Optional[str] = None
    sect: Optional[str] = None
    position: Optional[str] = None


class SpcPartEmployeeLoginRequest(BaseModel):
    employee_code: str = Field(..., max_length=50, description="Employee identifier")
    password: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Required when employee role is manage",
    )


class SpcPartEmployeeLoginResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    role: str
    employee: SpcPartEmployeeResponse
