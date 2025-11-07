from sqlalchemy.orm import Session
from app.models.spc_part_master_model import SpcPartMasterModel

def get_spc_part_master_all(db: Session, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size

    query = db.query(SpcPartMasterModel)

    total_items = query.count()


    data = (
        query.order_by(SpcPartMasterModel.Part_No.asc())
        .offset(skip)
        .limit(page_size)
        .all()
    )

    return data, total_items