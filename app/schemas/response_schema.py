from typing import Any, Optional, Generic, TypeVar, Union
from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_items: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")


class ApiResponse(BaseModel, Generic[T]):
    """
    ✅ Generic Response Model รองรับได้ทั้ง
       - Object เดียว
       - Dict ที่ซ้อนหลายระดับ
       - List ของข้อมูล
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    duration: str = Field(..., description="API execution time in seconds")
    resultData: Optional[Union[T, dict, list[Any]]] = Field(
        default=None,
        description="Response data (can be object, dict, or list)"
    )
    pagination: Optional[PaginationMeta] = None
    message: Optional[str] = None
