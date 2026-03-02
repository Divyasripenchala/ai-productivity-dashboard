# AI Productivity Dashboard (Backend)

## Overview
AI Productivity Dashboard is a FastAPI-based backend application that simulates factory productivity metrics. It calculates worker efficiency, workstation performance, and overall factory utilization.

This project demonstrates backend API development using Python and FastAPI.

---

## Tech Stack
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Git & GitHub

---

## Features
- Seed factory production data
- Calculate total units produced
- Compute factory utilization percentage
- Worker-level metrics
- Workstation-level metrics
- REST API endpoints
- Interactive API documentation (Swagger UI)

---

## API Endpoints
- `POST /seed`
- `GET /metrics`
- `GET /docs`

---

## How to Run

```bash
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload

Open:
http://127.0.0.1:8000/docs
