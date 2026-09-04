from fastapi import FastAPI

app = FastAPI(title="NFL Game Predictor")


@app.get("/health")
def health():
    return {"status": "healthy"}