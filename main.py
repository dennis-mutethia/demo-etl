
import asyncio
import logging

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.dialects.postgresql import insert

from routes import matches
from utils.betika import Betika
from utils.database import async_session, init_db
from utils.models import Matches

# Global logging configuration (applies to all modules)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Optional: Custom date format (e.g., 2025-11-04 22:13:45)
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="DEMO-ETL Backend", 
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Only your frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],  # Common needed headers
)

# Include all routers
app.include_router(matches.router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")



async def main():
    betika = Betika()
    total, page, data = betika.get_upcoming_matches()

    values = [
        {
            "match_id": int(m["match_id"]),
            "parent_match_id": int(m["parent_match_id"]),
            "game_id": int(m["game_id"]),
            "home_team": m["home_team"],
            "away_team": m["away_team"],
            "start_time": datetime.strptime(
                m["start_time"], "%Y-%m-%d %H:%M:%S"
            ),
            "competition_name": m["competition_name"],
            "category": m["category"],
            "side_bets": int(m["side_bets"]),
            "competition_id": int(m["competition_id"]),
            "sport_id": int(m["sport_id"]),
            "sport_name": m["sport_name"],
            "is_esport": bool(m["is_esport"]),
            "is_srl": bool(m["is_srl"]),
        }
        for m in data
    ]

    stmt = (
        insert(Matches)
        .values(values)
        .on_conflict_do_nothing(index_elements=["match_id"])
    )

    try:
        async with async_session() as session:
            await session.execute(stmt)
            await session.commit()
            logger.info("Processed `%s` matches", total)
    
    except Exception as err:
        logger.error(err)


if __name__ == "__main__":
    asyncio.run(main())
