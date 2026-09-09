"""
Run from backend/:
    python -m app.data.build_features
"""

import pandas as pd

from app.database import SessionLocal
from app import models

ROLLING_WINDOW = 5

def load_games_as_dataframe(db):
    games = db.query(models.Game).filter(models.Game.is_final == True).all()
    
    rows = []
    for game in games:
        rows.append({
            "game_id": game.game_id,
            "season": game.season,
            "week": game.week,
            "game_date": game.game_date,
            "team": game.home_team.abbreviation,
            "team_id": game.home_team.id,
            "opponent": game.away_team.abbreviation,
            "points_for": game.home_score,
            "points_against": game.away_score,
            "won": game.home_score > game.away_score,
            "is_home": True,
        })
        rows.append({
            "game_id": game.game_id,
            "season": game.season,
            "week": game.week,
            "game_date": game.game_date,
            "team": game.away_team.abbreviation,
            "team_id": game.away_team.id,
            "opponent": game.home_team.abbreviation,
            "points_for": game.away_score,
            "points_against": game.home_score,
            "won": game.away_score > game.home_score,
            "is_home": False,
        })
    
    return pd.DataFrame(rows)

def add_rolling_features(df):
    df = df.sort_values(by=["team", "game_date"]).reset_index(drop=True)
    df["rolling_points_for"] = (
        df.groupby("team")["points_for"]
        .transform(lambda x: x.shift(1).rolling(ROLLING_WINDOW, min_periods=1).mean())
    )
    df["rolling_points_against"] = (
        df.groupby("team")["points_against"]
        .transform(lambda x: x.shift(1).rolling(ROLLING_WINDOW, min_periods=1).mean())
    )
    df["rolling_win_pct"] = (
        df.groupby("team")["won"]
        .transform(lambda x: x.shift(1).rolling(ROLLING_WINDOW, min_periods=1).mean())
    )
    
    return df

def save_features(db, df):
    # Clear existing features
    deleted = db.query(models.TeamGameFeature).delete()
    db.commit()
    print(f"Cleared {deleted} existing feature rows")
        
    inserted = 0
    for _, row in df.iterrows():
        rpf = row["rolling_points_for"]
        rpa = row["rolling_points_against"]
        rwp = row["rolling_win_pct"]
        
        feature = models.TeamGameFeature(
            game_id=row["game_id"],
            team_id=int(row["team_id"]),
            is_home=bool(row["is_home"]),
            rolling_points_for=float(rpf) if pd.notnull(rpf) else None,
            rolling_points_against=float(rpa) if pd.notnull(rpa) else None,
            rolling_win_pct=float(row["rolling_win_pct"]) if pd.notnull(rwp) else None,
        )
        db.add(feature)
        inserted += 1
        
    db.commit()
    print(f"Inserted {inserted} new feature rows")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        long_df = load_games_as_dataframe(db)
        print(f"Loaded {len(long_df)} team-game rows from {long_df['game_id'].nunique()} games")
        
        featured_df = add_rolling_features(long_df)
        save_features(db, featured_df)
    finally:
        db.close()