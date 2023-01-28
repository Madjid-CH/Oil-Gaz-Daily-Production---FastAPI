from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database.database import get_db
from schemas import Well

router = APIRouter()


@router.get("/wells", response_model=list[Well])
async def get_wells(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wells = crud.get_wells(db, skip=skip, limit=limit)
    return wells


@router.get("/wells/{well_id}", response_model=schemas.Well)
async def get_well_by_id(well_id: int, db: Session = Depends(get_db)):
    db_well = crud.get_well(db, well_id=well_id)
    if db_well is None:
        raise HTTPException(status_code=400, detail="Well not found")
    return db_well


@router.post("/wells/new", response_model=schemas.Well)
async def create_well(well: schemas.WellCreate, db: Session = Depends(get_db)):
    db_well = crud.get_well_by_name(db, name=well.name)
    if db_well:
        raise HTTPException(status_code=400, detail="Well already exists")

    if well.field not in ("SOUTH", "NORTH", "CENTER"):
        raise HTTPException(status_code=400, detail="Field must be SOUTH, NORTH or CENTER")

    return crud.create_well(db=db, well=well)


@router.put("/wells/update/{id}", response_model=schemas.Well)
async def update_user(id: int, well: schemas.Well, db: Session = Depends(get_db)):
    db_well = crud.get_well(db, well_id=id)
    if db_well is None:
        raise HTTPException(status_code=400, detail="Well not found")
    well.id = id
    return crud.update_well(db=db, well=well)
