from fastapi import APIRouter, Query
from src.domain.song.schemas import SongResponse
from src.domain.song.services import get_songs_by_category

from typing import List

router = APIRouter()

@router.get("/list", response_model=List[SongResponse])
async def get_songs_by_category_api(category: str, page: int = Query(1, ge=1), size: int = Query(10, ge=1)):
    skip = (page - 1) * size
    songs = await get_songs_by_category(category, skip, size)
    return songs

'''
@router.post("/", response_model=SongResponse)
async def create_song_api(song: SongCreate):
    song_id = await create_song(song.dict())
    return {**song.dict(), "songid": song_id, "createdAt": datetime.now(), "modifiedAt": datetime.now()}

'''

'''
@router.get("/search", response_model=List[SongResponse])
async def search_songs_api(query: str, page: int = Query(1, ge=1), size: int = Query(10, ge=1)):
    skip = (page - 1) * size
    songs = await search_songs(query, skip, size)
    return songs
'''