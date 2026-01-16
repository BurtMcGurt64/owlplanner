"""
Create the FastAPI app
"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import courses, schedules
from app.services.loader import load_courses_from_csv

app = FastAPI(title="OwlPlanner API")

# Allow frontend to call this API (local dev + deployed)
# Allow both localhost and 127.0.0.1 dev URLs (Vite often picks different ports)
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:5176",
    "https://owlplanner.onrender.com",
    "https://owlplanner.vercel.app",
    "https://owlplanner-9ypnivlqr-burtmcgurt64s-projects.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
