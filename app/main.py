from fastapi import FastAPI
from app.database import engine
from app.models import Base

app = FastAPI(title="Gman", version="0.0.1")

@app.on_event("startup")
async def startup():
    '''
    creates tables on startup
    '''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


