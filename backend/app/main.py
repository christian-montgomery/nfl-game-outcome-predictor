from fastapi import FastAPI
from sqlalchemy import text

from app.database import Base, engine
from app import models

app = FastAPI(title="NFL Game Predictor")
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "database connection successful"}