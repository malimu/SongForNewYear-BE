from fastapi import APIRouter, HTTPException
from src.domain.wish.schemas import WishCreate, WishResponse
from src.domain.wish.services import create_wish, get_random_wishes

from typing import List, Optional

router = APIRouter()

@router.post("/", response_model=WishResponse)
async def create_wish_api(wish: WishCreate):
    wish_id = await create_wish(wish.nickname, wish.content, wish.songid)
    return {**wish.dict(), "wishId": wish_id, "isDisplayed": True, "createdAt": datetime.now()}

@router.get("/random", response_model=List[WishResponse])
async def get_random_wishes_api():
    wishes = await get_random_wishes()
    return wishes
