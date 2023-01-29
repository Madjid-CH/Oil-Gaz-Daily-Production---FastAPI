from datetime import datetime

import pytest

from app.models import Well, Material, DailyProduction
from database.database import SessionLocal


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    with SessionLocal() as db:
        empty_database(db)
        populate_database(db)
        yield
        empty_database(db)


def empty_database(db):
    db.query(Well).delete()
    db.query(Material).delete()
    db.query(DailyProduction).delete()
    db.commit()


def populate_database(db):
    add_wells(db)
    add_materials(db)
    add_daily_productions(db)


def add_wells(db):
    wells = [
        Well(name="well 1", field="NORTH"),
        Well(name="well 2", field="NORTH"),
        Well(name="well 3", field="CENTER"),
        Well(name="well 4", field="SOUTH"),
    ]

    db.add_all(wells)
    db.commit()


def add_materials(db):
    materials = [
        Material(name="oil", uom="M3"),
        Material(name="water", uom="M3"),
        Material(name="gas", uom="M3"),
    ]
    db.add_all(materials)
    db.commit()


def add_daily_productions(db):
    daily_productions = [
        DailyProduction(well_id=1, material_id=1, production_date=datetime(2023, 1, 2), qte=100),
        DailyProduction(well_id=1, material_id=1, production_date=datetime(2023, 1, 1), qte=100),
        DailyProduction(well_id=1, material_id=1, production_date=datetime(2023, 1, 3), qte=100),
        DailyProduction(well_id=2, material_id=2, production_date=datetime(2023, 1, 4), qte=100),
        DailyProduction(well_id=2, material_id=2, production_date=datetime(2023, 1, 5), qte=100),
        DailyProduction(well_id=2, material_id=2, production_date=datetime(2023, 1, 6), qte=100),
        DailyProduction(well_id=2, material_id=2, production_date=datetime(2023, 1, 7), qte=100),
        DailyProduction(well_id=3, material_id=3, production_date=datetime(2023, 1, 8), qte=100),
        DailyProduction(well_id=3, material_id=3, production_date=datetime(2023, 1, 9), qte=100),
        DailyProduction(well_id=3, material_id=3, production_date=datetime(2023, 1, 10), qte=100),
        DailyProduction(well_id=3, material_id=1, production_date=datetime(2023, 1, 10), qte=100),
    ]
    db.add_all(daily_productions)
    db.commit()
