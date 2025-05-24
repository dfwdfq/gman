from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import util, schemas
from app.database import get_db

router = APIRouter(prefix="/api")



@router.post("/graph/", response_model=schemas.GraphCreateResponse, status_code=201)
async def create_new_graph(graph: schemas.GraphCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await util.create_graph(db, graph)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"message": str(e)})
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail={"message": str(e)})

