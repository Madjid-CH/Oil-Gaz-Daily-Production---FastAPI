import enum

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, UniqueConstraint, Float  # type: ignore
from sqlalchemy import Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class MyEnum(enum.Enum):
    CENTER = 'CENTER'
    NORTH = 'NORTH'
    SOUTH = 'SOUTH'


class Well(Base):
    __tablename__ = "wells"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False, unique=True)
    field = Column(String, index=True, nullable=False)

    production = relationship("DailyProduction", back_populates="well")


class DailyProduction(Base):
    __tablename__ = "daily_productions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    production_date = Column(DateTime, nullable=False, default=func.current_date())
    well_id = Column(Integer, ForeignKey("wells.id"), nullable=False)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False)
    qte = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("production_date", "well_id", "material_id", name="uk_key"),
    )
    # Establish a bidirectional One-To-Many relationship
    well = relationship("Well", back_populates="production")
    material = relationship("Material", back_populates="production")


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False, unique=True)
    uom = Column(String, index=True, nullable=False)

    production = relationship("DailyProduction", back_populates="material")
