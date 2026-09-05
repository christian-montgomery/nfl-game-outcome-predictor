from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Team(Base):
    __tablename__ = "teams"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    abbreviation: Mapped[str] = mapped_column(String(5), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    
class Game(Base):
    __tablename__ = "games"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    season: Mapped[int] = mapped_column(Integer)
    week: Mapped[int] = mapped_column(Integer)
    game_date: Mapped[datetime] = mapped_column(DateTime)
    
    home_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    is_final: Mapped[bool] = mapped_column(Boolean, default=False)
    
    home_team: Mapped["Team"] = relationship("Team", foreign_keys=[home_team_id])
    away_team: Mapped["Team"] = relationship("Team", foreign_keys=[away_team_id])
    
class TeamGameFeature(Base):
    __tablename__ = "team_game_features"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[str] = mapped_column(ForeignKey("games.game_id"), index=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    
    is_home: Mapped[bool] = mapped_column(Boolean)
    
    rolling_points_for: Mapped[float | None] = mapped_column(Float, nullable=True)
    rolling_points_against: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    game: Mapped["Game"] = relationship("Game", backref="team_game_features")
    team: Mapped["Team"] = relationship("Team", backref="team_game_features")