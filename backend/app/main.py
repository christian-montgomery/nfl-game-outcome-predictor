from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine, SessionLocal
from app import models
from app.routers import games

app = FastAPI(title="NFL Game Predictor")
Base.metadata.create_all(bind=engine)

app.include_router(games.router)


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "database connection successful"}