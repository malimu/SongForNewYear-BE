from fastapi import APIRouter, HTTPException
from src.domain.wish.schemas import WishCreate, WishResponse, RecommendationResponse, SongRecommendation
from src.domain.wish.services import process_wish, get_random_wishes

from typing import List, Optional

router = APIRouter()

@router.post("", response_model=RecommendationResponse)
async def wish(wish: WishCreate):
    return await process_wish(wish)

@router.get("/random", response_model=List[WishResponse])
async def get_random_wishes_api(limit: int = 4):
    return await get_random_wishes(limit=limit)
