from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationMeta(BaseModel):
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_items: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")


class ApiResponse(BaseModel, Generic[T]):
    duration: str = Field(..., description="API execution time in seconds")
    resultData: Optional[T] = None
    pagination: Optional[PaginationMeta] = None
    message: Optional[str] = None
