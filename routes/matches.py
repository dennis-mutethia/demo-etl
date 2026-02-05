
from datetime import datetime
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from utils.models import Matches
from utils.database import get_session

router = APIRouter(prefix="/matches", tags=["Matches"])
    

@router.get("/")
async def get_matches(
    session: AsyncSession = Depends(get_session)
):
    statement = (
        select(Matches).order_by(Matches.start_time)
    )

    result = await session.execute(statement)
    matches = result.scalars().all()

    if not matches:
        raise HTTPException(status_code=404, detail="No Matches found")

    return matches
