from fastapi import FastAPI
from app.database import engine
from sqlalchemy import text

app = FastAPI(title="NFL Game Predictor")


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/db-test")
def db_test():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "database connection successful"}