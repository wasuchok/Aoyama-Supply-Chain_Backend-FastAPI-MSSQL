from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.spc_part_master_model import SpcPartMasterModel
from app.schemas.spc_part_master_schema import (
    PartInformationResponse,
    SpcPartMasterDetailResponse,
    SpcPartMasterResponse,
)

def get_spc_part_master_all(db: Session, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size

    query = db.query(SpcPartMasterModel)

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


