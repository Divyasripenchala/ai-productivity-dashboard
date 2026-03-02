from fastapi import FastAPI
from database import engine, Base, SessionLocal
from models import Worker, Workstation, Event
from datetime import datetime, timedelta

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "AI Productivity Dashboard Backend Running"}


@app.post("/seed")
def seed_data():
    db = SessionLocal()

    # Clear existing data
    db.query(Event).delete()
    db.query(Worker).delete()
    db.query(Workstation).delete()

    # Create workers
    workers = [
        Worker(worker_id=f"W{i}", name=f"Worker {i}")
        for i in range(1, 7)
    ]

    # Create workstations
    stations = [
        Workstation(station_id=f"S{i}", name=f"Station {i}")
        for i in range(1, 7)
    ]

    db.add_all(workers)
    db.add_all(stations)

    now = datetime.utcnow()

    # Sample events
    events = [
        Event(
            timestamp=now,
            worker_id="W1",
            workstation_id="S1",
            event_type="working",
            confidence=0.95,
            count=0
        ),
        Event(
            timestamp=now + timedelta(minutes=10),
            worker_id="W1",
            workstation_id="S1",
            event_type="idle",
            confidence=0.90,
            count=0
        ),
        Event(
            timestamp=now + timedelta(minutes=20),
            worker_id="W1",
            workstation_id="S1",
            event_type="product_count",
            confidence=0.98,
            count=15
        ),
    ]

    db.add_all(events)
    db.commit()
    db.close()

    return {"message": "Database seeded successfully"}


@app.get("/metrics")
def get_metrics():
    db = SessionLocal()

    workers = db.query(Worker).all()
    stations = db.query(Workstation).all()
    events = db.query(Event).filter(Event.confidence >= 0.9).all()

    worker_metrics = []
    workstation_metrics = []

    # Worker Metrics
    for worker in workers:
        worker_events = [e for e in events if e.worker_id == worker.worker_id]

        working_time = sum(10 for e in worker_events if e.event_type == "working")
        idle_time = sum(10 for e in worker_events if e.event_type == "idle")
        total_units = sum(e.count for e in worker_events if e.event_type == "product_count")

        utilization = 0
        if (working_time + idle_time) > 0:
            utilization = (working_time / (working_time + idle_time)) * 100

        worker_metrics.append({
            "worker_id": worker.worker_id,
            "worker_name": worker.name,
            "working_time_minutes": working_time,
            "idle_time_minutes": idle_time,
            "utilization_percent": round(utilization, 2),
            "total_units_produced": total_units
        })

    # Workstation Metrics
    for station in stations:
        station_events = [e for e in events if e.workstation_id == station.station_id]

        working_time = sum(10 for e in station_events if e.event_type == "working")
        idle_time = sum(10 for e in station_events if e.event_type == "idle")
        total_units = sum(e.count for e in station_events if e.event_type == "product_count")

        utilization = 0
        if (working_time + idle_time) > 0:
            utilization = (working_time / (working_time + idle_time)) * 100

        workstation_metrics.append({
            "station_id": station.station_id,
            "station_name": station.name,
            "working_time_minutes": working_time,
            "idle_time_minutes": idle_time,
            "utilization_percent": round(utilization, 2),
            "total_units_produced": total_units
        })

    # Factory Summary
    total_working_time = sum(w["working_time_minutes"] for w in worker_metrics)
    total_idle_time = sum(w["idle_time_minutes"] for w in worker_metrics)
    total_units = sum(w["total_units_produced"] for w in worker_metrics)

    factory_utilization = 0
    if (total_working_time + total_idle_time) > 0:
        factory_utilization = (total_working_time / (total_working_time + total_idle_time)) * 100

    db.close()

    return {
        "factory_summary": {
            "total_working_time_minutes": total_working_time,
            "total_idle_time_minutes": total_idle_time,
            "total_units_produced": total_units,
            "factory_utilization_percent": round(factory_utilization, 2)
        },
        "worker_metrics": worker_metrics,
        "workstation_metrics": workstation_metrics
    }