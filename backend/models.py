from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# -------------------------
# Workers Table
# -------------------------
class Worker(Base):
    __tablename__ = "workers"

    worker_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

    events = relationship("Event", back_populates="worker")


# -------------------------
# Workstations Table
# -------------------------
class Workstation(Base):
    __tablename__ = "workstations"

    station_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)

    events = relationship("Event", back_populates="workstation")


# -------------------------
# Events Table
# -------------------------
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    worker_id = Column(String, ForeignKey("workers.worker_id"))
    workstation_id = Column(String, ForeignKey("workstations.station_id"))
    event_type = Column(String, nullable=False)
    confidence = Column(Float)
    count = Column(Integer, default=0)

    worker = relationship("Worker", back_populates="events")
    workstation = relationship("Workstation", back_populates="events")