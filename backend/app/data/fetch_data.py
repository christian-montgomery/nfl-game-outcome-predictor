import nfl_data_py as nfl

from app.database import SessionLocal, Base, engine
from app import models

Base.metadata.create_all(bind=engine)

def load_teams(db):
    teams_df = nfl.import_team_desc()
    existing = {t.abbreviation for t in db.query(models.Team).all()}

    inserted = 0
    for _, row in teams_df.iterrows():
        abbr = row["team_abbr"]
        if abbr in existing:
            continue
        db.add(models.Team(abbreviation=abbr, name=row["team_name"]))
        inserted += 1

    db.commit()
    print(f"Inserted {inserted} new teams")
    
def load_games(db, seasons):
    schedules_df = nfl.import_schedules(seasons)
    team_lookup = {t.abbreviation: t.id for t in db.query(models.Team).all()}
    existing_game_ids = {g.game_id for g in db.query(models.Game).all()}

    inserted = 0
    for _, row in schedules_df.iterrows():
        if row["game_id"] in existing_game_ids:
            continue
        
        home_abbr = row["home_team"]
        away_abbr = row["away_team"]

        if home_abbr not in team_lookup or away_abbr not in team_lookup:
            print(f"Skipping {row['game_id']}: team not found ({home_abbr} or {away_abbr})")
            continue

        home_score = row["home_score"]
        away_score = row["away_score"]

        game = models.Game(
            game_id=row["game_id"],
            season=int(row["season"]),
            week=int(row["week"]),
            game_date=row["gameday"],
            home_team_id=team_lookup[home_abbr],
            away_team_id=team_lookup[away_abbr],
            home_score=int(home_score) if home_score == home_score else None,  # NaN check
            away_score=int(away_score) if away_score == away_score else None,
            is_final=home_score == home_score,  # not NaN means game is done
        )
        db.add(game)
        inserted += 1

    db.commit()
    print(f"Inserted {inserted} games")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        load_teams(db)
        load_games(db, seasons=[2023])
    finally:
        db.close()