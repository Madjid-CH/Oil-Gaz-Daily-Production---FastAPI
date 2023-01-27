import datetime

from pydantic import BaseModel


# Create Pydantic Base models with common attributes while creating or reading database.
class WellBase(BaseModel):
    name: str
    field: str


class DailyProductionBase(BaseModel):
    production_date: datetime.date
    qte: float


class MaterialBase(BaseModel):
    name: str
    uom: str


# create Pydantic models that will be used when reading database (returning it from the API)
class Well(WellBase):
    id: int

    class Config:
        orm_mode = True


class DailyProduction(DailyProductionBase):
    id: int
    well_id: int
    material_id: int

    class Config:
        orm_mode = True


class Material(MaterialBase):
    id: int

    class Config:
        orm_mode = True


# create Pydantic models needed for creation purposes
class WellCreate(WellBase):
    pass


class MaterialCreate(MaterialBase):
    pass


class DailyProductionCreate(DailyProductionBase):
    pass
