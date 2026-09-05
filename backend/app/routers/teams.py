from fastapi import APIRouter

from app.database import SessionLocal
from app import models

router = APIRouter()

@router.get("/teams")
def get_teams():
    db = SessionLocal()
    try:
        teams = db.query(models.Team).order_by(models.Team.abbreviation).all()
        return [
            {
                "id": t.id,
                "name": t.name,
                "abbreviation": t.abbreviation,
            }
            for t in teams
        ]
    finally:
        db.close()