"""
Pydantic models so FastAPI knows what data type to expect and return.
"""
from pydantic import BaseModel
from typing import List, Dict, Any

class SubjectsResponse(BaseModel):
    subjects: List[str]

class CoursesResponse(BaseModel):
    courses: List[Dict[str, Any]]
    
class ScheduleRequest(BaseModel):
    courses: List[str]  # e.g., ["COMP 140", "MATH 212"]

class ScheduleResponse(BaseModel):
    total: int
    schedules: List[List[Dict[str, Any]]]  # list of schedules; each schedule is list of section dicts

