import datetime

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database.database import get_db

router = APIRouter()


@router.get("/Productions/wells/{well_id}", response_model=list[schemas.DailyProduction])
async def get_daily_productions_by_well(well_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_well = crud.get_well(db, well_id=well_id)
    if db_well is None:
        raise HTTPException(status_code=400, detail="Well not found")

    daily_productions = crud.get_daily_production_by_well(db, well_id, skip, limit)
    return daily_productions


@router.get("/Productions/date/{prod_date}", response_model=list[schemas.DailyProduction])
async def get_daily_productions_by_date(prod_date: datetime.date, skip: int = 0, limit: int = 100,
                                        db: Session = Depends(get_db)):
    daily_productions = crud.get_daily_production_by_date(db, prod_date, skip, limit)
    return daily_productions


@router.post("/productions/new/{well_id}/{material_id}", response_model=schemas.DailyProduction)
async def create_production(well_id: int,
                            material_id: int,
                            production: schemas.DailyProductionCreate,
                            db: Session = Depends(get_db)):
    return crud.create_production(db=db, production=production, well_id=well_id, material_id=material_id)


@router.delete("/productions/delete/{material_name}/{well_id}/{prod_date}")
async def delete_production(material_name: str,
                            well_id: int,
                            prod_date: datetime.date,
                            db: Session = Depends(get_db)):
    db_prod = (
        db.query(models.DailyProduction)
        .join(models.Material)
        .filter(
            models.DailyProduction.well_id == well_id,
            models.Material.name == material_name,
            models.DailyProduction.production_date == datetime.datetime(prod_date.year, prod_date.month, prod_date.day)
        ).first()
    )
    if db_prod is None:
        raise HTTPException(status_code=400, detail="Well or Material or DailProduction not found")
    crud.delete_production(db=db, prod=db_prod)

    return {"msg": "Successfully Deleted"}
