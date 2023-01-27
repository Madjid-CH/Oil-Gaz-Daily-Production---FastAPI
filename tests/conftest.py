from datetime import datetime

import pytest

import models
from database.database import SessionLocal


@pytest.fixture(scope="module")
def setup_database():
    with SessionLocal() as db:
        db.query(models.Well).delete()
        db.query(models.Material).delete()
        db.query(models.DailyProduction).delete()
        db.commit()

        wells = [
            models.Well(name="well 1", field="NORTH"),
            models.Well(name="well 2", field="NORTH"),
            models.Well(name="well 3", field="CENTER"),
            models.Well(name="well 4", field="SOUTH"),
        ]
        db.add_all(wells)
        db.commit()

        materials = [
            models.Material(name="oil", uom="M3"),
            models.Material(name="water", uom="M3"),
            models.Material(name="gas", uom="M3"),
        ]
        db.add_all(materials)
        db.commit()

        daily_productions = [
            models.DailyProduction(well_id=1, material_id=1, production_date=datetime(2023, 1, 2), qte=100),
            models.DailyProduction(well_id=1, material_id=1, production_date=datetime(2023, 1, 1), qte=100),
            models.DailyProduction(well_id=1, material_id=1, production_date=datetime(2023, 1, 3), qte=100),
            models.DailyProduction(well_id=2, material_id=2, production_date=datetime(2023, 1, 4), qte=100),
            models.DailyProduction(well_id=2, material_id=2, production_date=datetime(2023, 1, 5), qte=100),
            models.DailyProduction(well_id=2, material_id=2, production_date=datetime(2023, 1, 6), qte=100),
            models.DailyProduction(well_id=2, material_id=2, production_date=datetime(2023, 1, 7), qte=100),
            models.DailyProduction(well_id=3, material_id=3, production_date=datetime(2023, 1, 8), qte=100),
            models.DailyProduction(well_id=3, material_id=3, production_date=datetime(2023, 1, 9), qte=100),
            models.DailyProduction(well_id=3, material_id=3, production_date=datetime(2023, 1, 10), qte=100),
            models.DailyProduction(well_id=3, material_id=1, production_date=datetime(2023, 1, 10), qte=100),
        ]
        db.add_all(daily_productions)
        db.commit()

        yield db

        db.query(models.Well).delete()
        db.query(models.Material).delete()
        db.query(models.DailyProduction).delete()
        db.commit()
