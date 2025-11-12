
import hashlib

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.spc_part_role import SpcPartRoleModel
from app.schemas.spc_part_employee_schema import (
    SpcPartEmployeeLoginRequest,
    SpcPartEmployeeLoginResponse,
    SpcPartEmployeeResponse,
)
from app.schemas.spc_part_role_schema import (
    SpcPartRoleRequest,
    SpcPartRoleResponse,
)


def _hash_password(raw_password: str | None) -> str | None:
    if raw_password is None:
        return None
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def get_spc_part_employee(db: Session, employee_code: str):
    sql = text("""
        SELECT
            V_Employee.*,
            Tb_Spc_Part_Role.role
        FROM V_Employee
        LEFT JOIN Tb_Spc_Part_Role
            ON Tb_Spc_Part_Role.emp_no = V_Employee.id
        WHERE V_Employee.id = :employee_code
    """)

    result_raw = db.execute(sql, {"employee_code": employee_code})
    rows = [dict(row._mapping) for row in result_raw]

    if not rows:
        return None

    data = rows[0]

    if data.get("role") is None:
        data["role"] = "employee"

    return data


def add_role_manage(db: Session, payload: SpcPartRoleRequest) -> SpcPartRoleResponse:
    hashed_password = _hash_password(payload.password)

    role_record = (
        db.query(SpcPartRoleModel)
        .filter(SpcPartRoleModel.emp_no == payload.emp_no)
        .first()
    )

    if role_record:
        role_record.role = payload.role
        if hashed_password is not None:
            role_record.password = hashed_password
    else:
        role_record = SpcPartRoleModel(
            emp_no=payload.emp_no,
            role=payload.role,
            password=hashed_password,
        )
        db.add(role_record)

    db.commit()
    db.refresh(role_record)
    return SpcPartRoleResponse.model_validate(role_record)


def login_spc_part_employee(
    db: Session, payload: SpcPartEmployeeLoginRequest
) -> SpcPartEmployeeLoginResponse:
    employee = get_spc_part_employee(db, payload.employee_code)
    if not employee:
        raise ValueError("Employee not found")

    role_record: SpcPartRoleModel | None = (
        db.query(SpcPartRoleModel)
        .filter(SpcPartRoleModel.emp_no == payload.employee_code)
        .first()
    )

    record_role = role_record.role if role_record else None
    role = record_role or employee.get("role") or "employee"
    requires_password = bool(record_role and record_role.lower() == "manage")

    if requires_password:
        if not payload.password:
            raise PermissionError("Password is required for manage role")
        hashed_input = _hash_password(payload.password)
        if not role_record.password or role_record.password != hashed_input:
            raise PermissionError("Invalid credentials")
    # Password is optional for non-manage roles; ignore if provided.

    subject = str(employee.get("id") or payload.employee_code)
    token = create_access_token(
        subject=subject,
        data={"emp_no": payload.employee_code, "role": role},
    )

    employee_payload = dict(employee)
    employee_payload["role"] = role

    return SpcPartEmployeeLoginResponse(
        access_token=token,
        role=role,
        employee=SpcPartEmployeeResponse.model_validate(employee_payload),
    )




