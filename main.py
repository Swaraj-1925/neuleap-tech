from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db import init_db
from  app.api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/",description="Initial routes")
def read_root():
    return {"message": "Wellcome "}

@app.get("/health",description="Health check")
def health():
    return {"status": "ok"}

