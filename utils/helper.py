from datetime import datetime

from utils.models import Matches

def build_match(match_data):
    return Matches(
        match_id=int(match_data.get("match_id")),
        parent_match_id=int(match_data.get("parent_match_id")),
        game_id=int(match_data.get("game_id")),
        home_team=match_data.get("home_team"),
        away_team=match_data.get("away_team"),
        start_time=datetime.strptime(match_data.get("start_time"), "%Y-%m-%d %H:%M:%S"),
        competition_name=match_data.get("competition_name"),
        category=match_data.get("category"),
        side_bets=int(match_data.get("side_bets")),
        competition_id=int(match_data.get("competition_id")),
        sport_id=int(match_data.get("sport_id")),
        sport_name=match_data.get("sport_name"),
        is_esport=bool(match_data.get("is_esport")),
        is_srl=bool(match_data.get("is_srl"))
    )
