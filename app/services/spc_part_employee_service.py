
from sqlalchemy import text
from sqlalchemy.orm import Session

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

