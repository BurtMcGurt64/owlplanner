"""
This router is the endpoint for the schedule generator.
"""

from fastapi import APIRouter, HTTPException
from app.schemas import ScheduleRequest, ScheduleResponse
from csv_parser import parse_csv
from scheduler import generate_schedule

router = APIRouter()

@router.post("/schedules", response_model = ScheduleResponse)
def create_schedule(payload: ScheduleRequest):
    if not payload.courses:
        raise HTTPException(status_code=400, detail="No courses provided")
    
    # parse the requested courses
    sections = parse_csv("course_data.csv", payload.courses)
    
    courses_by_name = {}
    for sec in sections:
        courses_by_name.setdefault(sec.course_name, []).append(sec)
    
    # ENSURE THER EIS AT LEAST ONE SECTION PER COURSE
    missing = [course for course in payload.courses if course not in courses_by_name]
    if missing:
        raise HTTPException(status_code=404, detail=f"Coruses not found: {', '.join(missing)}")
    
    # generate schedules
    schedules = generate_schedule(courses_by_name)

    # convert to dicts for JSON
    def section_to_dict(sec):
        return {
            "course" : sec.course_name,
            "crn" : sec.crn,
            "instructor" : sec.instructor,
            "meeting_times" : [
                {
                    "day" : mt.day,
                    "start" : mt.start,
                    "end" : mt.end,
                }
                for mt in sec.meeting_times
            ],
        }

    schedules_dict = [[section_to_dict(sec) for sec in schedule] for schedule in schedules]

    return ScheduleResponse(total=len(schedules_dict), schedules=schedules_dict)
