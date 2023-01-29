from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from app import crud, schemas
from database.database import get_db

router = APIRouter()


@router.get("/materials", response_model=list[schemas.Material])
async def get_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    materials = crud.get_materials(db, skip=skip, limit=limit)
    return materials


@router.get("/materials/{name}", response_model=schemas.Material)
async def get_material_by_name(name: str, db: Session = Depends(get_db)):
    db_material = crud.get_material_by_name(db, name=name)
    if db_material is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Material not found")
    return db_material


@router.post("/materials/new", response_model=schemas.Material)
async def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_material = crud.get_material_by_name(db, material.name)
    if db_material:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Material already exists")

    if material.uom not in ("M3", "Tonne"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="UOM must be M3 or Tonne")

    return crud.create_material(db=db, material=material)
