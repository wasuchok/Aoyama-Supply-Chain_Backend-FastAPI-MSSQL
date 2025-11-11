from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
class SpcPartEmployeeResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    efname: Optional[str] = None
    elname: Optional[str] = None
    sect: Optional[str] = None
    position: Optional[str] = None