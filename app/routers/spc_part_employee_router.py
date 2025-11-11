import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.response_schema import ApiResponse
from app.services.spc_part_employee_service import get_spc_part_employee
from app.schemas.spc_part_employee_schema import SpcPartEmployeeResponse
router = APIRouter(prefix="/spc-part-employee", tags=["Spc Part Employee"])

@router.get("/employee/{employee_code}", response_model=ApiResponse[SpcPartEmployeeResponse])
def read_spc_part_employee(employee_code: str, db: Session = Depends(get_db)):
    start_time = time.perf_counter()
    data = get_spc_part_employee(db, employee_code)
    duration = f"{(time.perf_counter() - start_time):.3f}s"
    return ApiResponse(duration=duration, resultData=data)