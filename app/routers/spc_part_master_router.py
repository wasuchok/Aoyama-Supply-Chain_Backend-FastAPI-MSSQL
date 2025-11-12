import time
from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.response_schema import ApiResponse, PaginationMeta
from app.schemas.spc_part_master_schema import (
    SpcPartMasterDetailResponse,
    SpcPartMasterResponse,
)
from app.services.spc_part_master_service import get_amount_production_by, get_spc_part_master_all, get_spc_part_master_by_part_no

router = APIRouter(prefix="/spc-part-master", tags=["Spc Part Master"])

@router.get("/", response_model=ApiResponse[List[SpcPartMasterResponse]])
def read_spc_part_masters(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: str | None = Query(None, description="Search keyword (search all fields)"),
    large: str | None = Query(None, description="Filter by Large level"),
    medium: str | None = Query(None, description="Filter by Medium level"),
    small: str | None = Query(None, description="Filter by Small level"),
    production_by: str | None = Query(None, description="Filter by Production_By"),
):
    start_time = time.perf_counter()


    data, total_items = get_spc_part_master_all(
        db,
        page=page,
        page_size=page_size,
        search=search,
        large=large,
        medium=medium,
        small=small,
        production_by=production_by,
    )

    total_pages = (total_items + page_size - 1) // page_size
    pagination = PaginationMeta(
        page=page, page_size=page_size, total_items=total_items, total_pages=total_pages
    )

    duration = f"{(time.perf_counter() - start_time):.3f}s"

    return ApiResponse(duration=duration, resultData=data, pagination=pagination)

@router.get("/levels")
def get_part_levels(
    db: Session = Depends(get_db),
    large: str | None = Query(None, description="Filter by Large category"),
    medium: str | None = Query(None, description="Filter by Medium category"),
):
    # ✅ Case 1: ไม่มี params → ดึง Large ทั้งหมด
    if large is None:
        sql = text("""
            SELECT DISTINCT Large
            FROM Tb_Spc_Part_Master
            WHERE Large IS NOT NULL
            ORDER BY Large
        """)
        result = db.execute(sql)
        data = [row[0] for row in result]
        return {"level": "large", "resultData": data}

    # ✅ Case 2: มี large แต่ไม่มี medium → ดึง Medium
    if medium is None:
        sql = text("""
            SELECT DISTINCT Medium
            FROM Tb_Spc_Part_Master
            WHERE Large = :large
              AND Medium IS NOT NULL
            ORDER BY Medium
        """)
        result = db.execute(sql, {"large": large})
        data = [row[0] for row in result]
        return {"level": "medium", "parent": large, "resultData": data}

    # ✅ Case 3: มีทั้ง large และ medium → ดึง Small
    sql = text("""
        SELECT DISTINCT Small
        FROM Tb_Spc_Part_Master
        WHERE Large = :large
          AND Medium = :medium
          AND Small IS NOT NULL
        ORDER BY Small
    """)
    result = db.execute(sql, {"large": large, "medium": medium})
    data = [row[0] for row in result]
    return {
        "level": "small",
        "parent": {"large": large, "medium": medium},
        "resultData": data
    }

@router.get("/{part_no}", response_model=ApiResponse[SpcPartMasterDetailResponse])
def read_spc_part_master_by_part_no(
    part_no: str,
    db: Session = Depends(get_db),
):
    start_time = time.perf_counter()


    data = get_spc_part_master_by_part_no(db, part_no=part_no)


    duration = f"{(time.perf_counter() - start_time):.3f}s"

    return ApiResponse(duration=duration, resultData=data)

@router.get("/statistics/production-by", response_model=ApiResponse[List[dict]])
def read_amount_production_by(
    db: Session = Depends(get_db),
):
    start_time = time.perf_counter()


    data = get_amount_production_by(db)


    duration = f"{(time.perf_counter() - start_time):.3f}s"

    return ApiResponse(duration=duration, resultData=data)

