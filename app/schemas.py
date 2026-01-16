"""
Pydantic models so FastAPI knows what data type to expect and return.
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SubjectsResponse(BaseModel):
    subjects: List[str]

class CoursesResponse(BaseModel):
    courses: List[Dict[str, Any]]
    
class ScheduleRequest(BaseModel):
    courses: List[str]  # e.g., ["COMP 140", "MATH 212"]
    preferences: Optional[Dict[str, bool]] = None  # e.g., {"morning_preference": True}

class ScheduleResponse(BaseModel):
    total: int
    schedules: List[Dict[str, Any]]  # Each item: {"score": float, "courses": [...]}

