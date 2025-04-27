import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"status": "ok"}
