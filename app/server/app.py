from fastapi import FastAPI

from app.server.routes.book import router as BookRouter

app = FastAPI()

app.include_router(BookRouter, tags=["Book"], prefix="/book")

@app.get("/", tags=["Root"])
async def hello_world():
    return {"message":"hello world!!!"}