from fastapi import FastAPI
from api import router

app = FastAPI(title="Intern Activity Tracker")

app.include_router(router)

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Intern Activity Tracker API is running"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
