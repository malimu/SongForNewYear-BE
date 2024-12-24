from fastapi import APIRouter, Query
from src.domain.song.schemas import PaginatedResponse
from src.domain.song.services import get_songs_by_category, get_total_songs_count
from typing import Optional

router = APIRouter()

@router.get("/list", response_model=PaginatedResponse)
async def get_songs_by_category_api(
    category: Optional[str] = None,  # category를 선택적으로 지정
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1)
):
    skip = (page - 1) * size
    songs = await get_songs_by_category(category, skip, size)
    total_items = await get_total_songs_count(category)
    total_pages = (total_items + size - 1) // size  # 전체 페이지 수 계산 (올림 처리)

    return PaginatedResponse(
        total_pages=total_pages,
        current_page=page,
        page_size=size,
        total_items=total_items,
        data=songs
    )