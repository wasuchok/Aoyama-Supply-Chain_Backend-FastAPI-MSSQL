import time
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.response_schema import ApiResponse, PaginationMeta
from app.schemas.spc_part_master_schema import SpcPartMasterResponse
from app.services.spc_part_master_service import get_spc_part_master_all

router = APIRouter(prefix="/spc-part-master", tags=["Spc Part Master"])

@router.get("/", response_model=ApiResponse[List[SpcPartMasterResponse]])
def read_spc_part_masters(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
):
    start_time = time.perf_counter()


    data, total_items = get_spc_part_master_all(db, page=page, page_size=page_size)


    total_pages = (total_items + page_size - 1) // page_size
    pagination = PaginationMeta(
        page=page, page_size=page_size, total_items=total_items, total_pages=total_pages
    )

    duration = f"{(time.perf_counter() - start_time):.3f}s"

    return ApiResponse(duration=duration, resultData=data, pagination=pagination)