from fastapi import APIRouter, HTTPException, Query
from src.domain.song.schemas import SongCreate, SongResponse
from src.domain.song.services import create_song, get_songs_by_category, search_songs

from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=SongResponse)
async def create_song_api(song: SongCreate):
    song_id = await create_song(song.dict())
    return {**song.dict(), "songid": song_id, "createdAt": datetime.now(), "modifiedAt": datetime.now()}

@router.get("/category/{category}", response_model=List[SongResponse])
async def get_songs_by_category_api(category: str, page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    skip = (page - 1) * limit
    songs = await get_songs_by_category(category, skip, limit)
    return songs

@router.get("/search", response_model=List[SongResponse])
async def search_songs_api(query: str, page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    skip = (page - 1) * limit
    songs = await search_songs(query, skip, limit)
    return songs
