import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.response_schema import ApiResponse
from app.services.spc_part_employee_service import (
    add_role_manage,
    get_spc_part_employee,
    login_spc_part_employee,
)
from app.schemas.spc_part_employee_schema import (
    SpcPartEmployeeLoginRequest,
    SpcPartEmployeeLoginResponse,
    SpcPartEmployeeResponse,
)
from app.schemas.spc_part_role_schema import (
    SpcPartRoleRequest,
    SpcPartRoleResponse,
)

router = APIRouter(prefix="/spc-part-employee", tags=["Spc Part Employee"])


@router.get("/employee/{employee_code}", response_model=ApiResponse[SpcPartEmployeeResponse])
def read_spc_part_employee(employee_code: str, db: Session = Depends(get_db)):
    start_time = time.perf_counter()
    data = get_spc_part_employee(db, employee_code)
    duration = f"{(time.perf_counter() - start_time):.3f}s"
    return ApiResponse(duration=duration, resultData=data)


@router.post("/manage-role", response_model=ApiResponse[SpcPartRoleResponse])
def manage_role(payload: SpcPartRoleRequest, db: Session = Depends(get_db)):
    start_time = time.perf_counter()
    data = add_role_manage(db, payload)
    duration = f"{(time.perf_counter() - start_time):.3f}s"
    return ApiResponse(duration=duration, resultData=data, message="Role saved successfully")


@router.post("/login", response_model=ApiResponse[SpcPartEmployeeLoginResponse])
def login(payload: SpcPartEmployeeLoginRequest, db: Session = Depends(get_db)):
    start_time = time.perf_counter()
    try:
        data = login_spc_part_employee(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)
        ) from exc
    duration = f"{(time.perf_counter() - start_time):.3f}s"
    return ApiResponse(duration=duration, resultData=data, message="Login successful")
