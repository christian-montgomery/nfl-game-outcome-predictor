from fastapi import APIRouter

from app.database import SessionLocal
from app import models

router = APIRouter()


@router.get("/games")
def get_games(season: int | None = None, week: int | None = None):
    db = SessionLocal()
    try:
        query = db.query(models.Game)
        if season is not None:
            query = query.filter(models.Game.season == season)
        if week is not None:
            query = query.filter(models.Game.week == week)

        games = query.order_by(models.Game.game_date).all()

        return [
            {
                "game_id": g.game_id,
                "season": g.season,
                "week": g.week,
                "date": g.game_date,
                "home_team": g.home_team.abbreviation,
                "away_team": g.away_team.abbreviation,
                "home_score": g.home_score,
                "away_score": g.away_score,
                "is_final": g.is_final,
            }
            for g in games
        ]
    finally:
        db.close()