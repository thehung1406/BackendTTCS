from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from mako.ext.autohandler import autohandler

from app.core.config import settings
from app.core.database import init_db
import uvicorn
import logging
from app.core.redis import redis_client
from app.router.auth import router as auth_router
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="BackendTTCS API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/redis-test")
def redis_test():
    redis_client.set("hello", "world")
    return {"value": redis_client.get("hello")}


app.include_router(auth_router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
