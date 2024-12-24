from fastapi import APIRouter, Query
from src.domain.song.schemas import PaginatedResponse
from src.domain.song.services import get_songs_by_category, get_total_songs_count

router = APIRouter()

@router.get("/list", response_model=PaginatedResponse)
async def get_songs_by_category_api(category: str, page: int = Query(1, ge=1), size: int = Query(10, ge=1)):
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

'''
@router.post("/", response_model=SongResponse)
async def create_song_api(song: SongCreate):
    song_id = await create_song(song.dict())
    return {**song.dict(), "song_id": song_id, "created_at": datetime.now(), "modified_at": datetime.now()}

'''

'''
@router.get("/search", response_model=List[SongResponse])
async def search_songs_api(query: str, page: int = Query(1, ge=1), size: int = Query(10, ge=1)):
    skip = (page - 1) * size
    songs = await search_songs(query, skip, size)
    return songs
'''