from typing import Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field

class Matches(SQLModel, table=True):
    match_id: int = Field(default=None, primary_key=True)
    parent_match_id: int
    game_id: int
    home_team: str
    away_team: str
    start_time: datetime
    competition_name: str
    category: str
    side_bets: int
    competition_id: int
    sport_id: int
    sport_name: str
    is_esport: bool
    is_srl: bool

