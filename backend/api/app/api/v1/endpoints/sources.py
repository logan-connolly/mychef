from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.db.repositories.sources import SourcesRepository
from app.db.session import get_db
from app.schemas.sources import InSourceSchema, SourceSchema

router = APIRouter()


@router.post("/", response_model=SourceSchema, status_code=HTTP_201_CREATED)
async def add_source(payload: InSourceSchema, db: AsyncSession = Depends(get_db)):
    repo = SourcesRepository(db)
    return await repo.create(payload)


@router.get("/{source_id}/", response_model=SourceSchema, status_code=HTTP_200_OK)
async def get_source(source_id: int, db: AsyncSession = Depends(get_db)):
    repo = SourcesRepository(db)
    return await repo.get_by_id(source_id)


@router.get("/", response_model=list[SourceSchema], status_code=HTTP_200_OK)
async def get_sources(db: AsyncSession = Depends(get_db)):
    repo = SourcesRepository(db)
    return await repo.get_all()
