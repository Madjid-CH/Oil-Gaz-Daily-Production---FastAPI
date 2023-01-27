import datetime

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    with SessionLocal() as db:
        yield db


@app.get("/wells", response_model=list[schemas.Well])
async def get_wells(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wells = crud.get_wells(db, skip=skip, limit=limit)
    return wells


@app.get("/wells/{id}", response_model=schemas.Well)
async def get_well_by_id(well_id: int, db: Session = Depends(get_db)):
    db_well = crud.get_well(db, well_id=well_id)
    if db_well is None:
        raise HTTPException(status_code=404, detail="Well not found")
    return db_well


@app.get("/materials", response_model=list[schemas.Material])
async def get_materials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    materials = crud.get_materials(db, skip=skip, limit=limit)
    return materials


@app.get("/materials/{name}", response_model=schemas.Material)
async def get_material_by_name(name: str, db: Session = Depends(get_db)):
    db_material = crud.get_material_by_name(db, name=name)
    if db_material is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return db_material


@app.get("/Productions/wells/{well_id}", response_model=list[schemas.DailyProduction])
async def get_daily_productions_by_well(well_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_well = crud.get_well(db, well_id=well_id)
    if db_well is None:
        raise HTTPException(status_code=404, detail="Well not found")

    daily_productions = crud.get_daily_production_by_well(db, well_id, skip, limit)
    return daily_productions


@app.get("/Productions/date/{prod_date}", response_model=list[schemas.DailyProduction])
async def get_daily_productions_by_date(prod_date: datetime.date, skip: int = 0, limit: int = 100,
                                        db: Session = Depends(get_db)):
    daily_productions = crud.get_daily_production_by_date(db, prod_date, skip, limit)
    return daily_productions


@app.post("/wells/new", response_model=schemas.Well)
async def create_well(well: schemas.WellCreate, db: Session = Depends(get_db)):
    db_well = crud.get_well_by_name(db, name=well.name)
    if db_well:
        raise HTTPException(status_code=400, detail="Well already exists")

    if well.field not in ("SOUTH", "NORTH", "CENTER"):
        raise HTTPException(status_code=400, detail="Field must be SOUTH, NORTH or CENTER")

    return crud.create_well(db=db, well=well)


@app.post("/materials/new", response_model=schemas.Material)
async def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_material = crud.get_material_by_name(db, material.name)
    if db_material:
        raise HTTPException(status_code=400, detail="Material already exists")

    if material.uom not in ("M3", "Tonne"):
        raise HTTPException(status_code=400, detail="UOM must be M3 or Tonne")

    return crud.create_material(db=db, material=material)


@app.post("/productions/new/{well_id}/{material_id}", response_model=schemas.DailyProduction)
async def create_production(well_id: int,
                            material_id: int,
                            production: schemas.DailyProductionCreate,
                            db: Session = Depends(get_db)):
    return crud.create_production(db=db, production=production, well_id=well_id, material_id=material_id)


@app.delete("/productions/delete/{material_name}/{well_id}/{prod_date}")
async def delete_post_for_user(material_name: str,
                               well_id: int,
                               prod_date: datetime.date,
                               db: Session = Depends(get_db)):
    db_prod = (db.query(models.DailyProduction)
               .filter(
        models.DailyProduction.well_id == well_id,
        models.Material.name == material_name,
        models.DailyProduction.prod_date == prod_date
    ).first())
    if db_prod is None:
        raise HTTPException(status_code=404, detail="Well or Material or DailProduction not found")
    crud.delete_production(db=db, prod=db_prod)
    return {"msg": "Successfully Deleted"}


@app.put("/wells/update/{id}", response_model=schemas.Well)
async def update_user(id: int, well: schemas.Well, db: Session = Depends(get_db)):
    db_well = crud.get_well(db, well_id=id)
    if db_well is None:
        raise HTTPException(status_code=404, detail="Well not found")
    well.id = id
    return crud.update_well(db=db, well=well)


if __name__ == '__main__':
    uvicorn.run(app)
