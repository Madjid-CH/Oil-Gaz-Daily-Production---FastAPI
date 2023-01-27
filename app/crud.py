from sqlalchemy.orm import Session

import models, schemas


def get_well(db: Session, well_id: int):
    return db.query(models.Well).filter(models.Well.id == well_id).first()


def get_wells(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Well).offset(skip).limit(limit).all()


def create_well(db: Session, well: schemas.WellCreate):
    db_well = models.Well(name=well.name, field=well.field)
    db.add(db_well)
    db.commit()
    db.refresh(db_well)
    return db_well


def create_production(db: Session, production: schemas.DailyProductionCreate, well_id: int, material_id: int):
    db_prod = models.DailyProduction(**production.dict(), well_id=well_id, material_id=material_id)
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod


def delete_production(db: Session, prod: schemas.DailyProduction):
    db.delete(prod)
    db.commit()


def get_daily_production_by_well(db, well_id, skip, limit):
    return db \
        .query(models.DailyProduction) \
        .filter(models.DailyProduction.well_id == well_id) \
        .offset(skip) \
        .limit(limit) \
        .all()


def update_well(db: Session, well: schemas.Well):
    db_well = get_well(db, well.id)
    db_well.name = well.name
    db_well.field = well.field
    db.commit()
    db.refresh(db_well)
    return db_well


def get_well_by_name(db, name):
    return db.query(models.Well).filter(models.Well.name == name).first()


def get_materials(db, skip, limit):
    return db.query(models.Material).offset(skip).limit(limit).all()


def get_material_by_name(db, name):
    return db.query(models.Material).filter(models.Material.name == name).first()


def get_daily_production_by_date(db, date, skip, limit):
    return db.query(models.DailyProduction) \
        .filter(models.DailyProduction.production_date == date) \
        .offset(skip) \
        .limit(limit) \
        .all()


def create_material(db, material):
    db_material = models.Material(name=material.name, uom=material.uom)
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material
