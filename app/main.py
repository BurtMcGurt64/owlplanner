"""
Create the FastAPI app
"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import courses, schedules
from app.services.loader import load_courses_from_csv

app = FastAPI(title="OwlPlanner API")

@app.get("/")
def root():
    # Send users to the interactive docs when hitting the base URL
    return RedirectResponse(url="/docs")

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(courses.router, prefix="/api")
app.include_router(schedules.router, prefix="/api")

# load the courses from csv on startup
@app.on_event("startup")
def startup():
    try:
        count = load_courses_from_csv("course_data.csv")
        print(f"[startup] Loaded {count} course rows into cache.")
    except FileNotFoundError:
        print("[startup] course_data.csv not found, run the scraper first.")
