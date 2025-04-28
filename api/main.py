import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routes import stats_router, weather_router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(stats_router, prefix="/stats")
app.include_router(weather_router, prefix="/weather")


@app.get("/")
async def read_root():
    return {"status": "ok"}
