from fastapi import FastAPI, HTTPException, Depends
from app.core.database import init_db
import uvicorn

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BackendTTCS API",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return {"message": "FastAPI running with Docker 🚀"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
