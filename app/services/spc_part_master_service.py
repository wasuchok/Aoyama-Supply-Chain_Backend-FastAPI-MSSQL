from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.spc_part_master_model import SpcPartMasterModel
from app.schemas.spc_part_master_schema import (
    PartInformationResponse,
    SpcPartMasterDetailResponse,
    SpcPartMasterResponse,
)

def get_spc_part_master_all(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    search: str | None = None,
    large: str | None = None,
    medium: str | None = None,
    small: str | None = None,
    production_by: str | None = None,
):
    skip = (page - 1) * page_size

    query = db.query(SpcPartMasterModel)

    if large:
        query = query.filter(SpcPartMasterModel.Large == large)

    if medium:
        query = query.filter(SpcPartMasterModel.Medium == medium)

    if small:
        query = query.filter(SpcPartMasterModel.Small == small)

    if production_by:
        query = query.filter(SpcPartMasterModel.Production_By == production_by)

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            or_(
                SpcPartMasterModel.Part_No.like(like_pattern),
                SpcPartMasterModel.Part_Name.like(like_pattern),
                SpcPartMasterModel.Mat_Name.like(like_pattern),
                SpcPartMasterModel.Diameter.like(like_pattern),
                SpcPartMasterModel.M_Size.like(like_pattern),
                SpcPartMasterModel.Small.like(like_pattern),
                SpcPartMasterModel.Medium.like(like_pattern),
                SpcPartMasterModel.Large.like(like_pattern),
                SpcPartMasterModel.Surface.like(like_pattern),
                SpcPartMasterModel.Production_By.like(like_pattern),
                SpcPartMasterModel.Update_By.like(like_pattern),
            )
        )

    total_items = query.count()


    items = (
        query.order_by(SpcPartMasterModel.Part_No.asc())
        .offset(skip)
        .limit(page_size)
        .all()
    )

    data = [SpcPartMasterResponse.model_validate(item) for item in items]

    return data, total_items



def get_spc_part_master_by_part_no(db: Session, part_no: str):

    result = db.query(SpcPartMasterModel).filter(
        SpcPartMasterModel.Part_No == part_no
    ).first()

    if not result:
        print(f"❌ ไม่พบข้อมูลใน SpcPartMasterModel สำหรับ Part_No: {part_no}")
        return SpcPartMasterDetailResponse(PartMaster=None, PartInformation=[])

    part_master = SpcPartMasterResponse.model_validate(result)


    sql = text("""
        SELECT *
        FROM V_Spc_Part_Information
        WHERE Part_No = :part_no
    """)
    result_raw = db.execute(sql, {"part_no": part_no})
    rows = [
        PartInformationResponse.model_validate(dict(row._mapping))
        for row in result_raw
    ]


    print(f"✅ พบข้อมูล PartMaster: {part_master.Part_No} | รายการใน PartInformation: {len(rows)} แถว")


    return SpcPartMasterDetailResponse(
        PartMaster=part_master,
        PartInformation=rows,
    )

def get_amount_production_by(db : Session) :
    sql = text("""
        SELECT Production_By, COUNT(*) AS Amount
        FROM Tb_Spc_Part_Master
        GROUP BY Production_By
    """)
    result_raw = db.execute(sql)
    result = [dict(row._mapping) for row in result_raw]
    return result


def get_part_levels(db: Session, large: str | None = None, medium: str | None = None):
    if large is None:
        sql = text("SELECT DISTINCT Large FROM Tb_Spc_Part_Master WHERE Large IS NOT NULL ORDER BY Large")
        result = db.execute(sql)
    elif medium is None:
        sql = text("""
            SELECT DISTINCT Medium
            FROM Tb_Spc_Part_Master
            WHERE Large = :large AND Medium IS NOT NULL
            ORDER BY Medium
        """)
        result = db.execute(sql, {"large": large})
    else:
        sql = text("""
            SELECT DISTINCT Small
            FROM Tb_Spc_Part_Master
            WHERE Large = :large AND Medium = :medium AND Small IS NOT NULL
            ORDER BY Small
        """)
        result = db.execute(sql, {"large": large, "medium": medium})

    return [row[0] for row in result]
