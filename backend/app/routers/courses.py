"""
This router provides endpoints related to course data.
"""

from fastapi import APIRouter, Query
from app.services.loader import get_courses
from app.schemas import SubjectsResponse, CoursesResponse

router = APIRouter()

@router.get("/subjects", response_model = SubjectsResponse)
def list_subjects():
    rows = get_courses()
    subjects = sorted({r["course"].split()[0] for r in rows if r.get("course")})
    return {"subjects" : subjects}

@router.get("/courses", response_model=CoursesResponse)
def list_courses(query: str = Query("", description = "Substring match on course name")):
    rows = get_courses()
    q = query.strip().lower()
    if not q:
        return {"courses" : rows}
    filtered = [r for r in rows if q in r["course"].lower()]
    return {"courses" : filtered}

