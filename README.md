# OwlPlanner
## Overview
This is a web application that generates and ranks all valid course schedules for Rice University students given a selection of courses, based on time constraints and user preferences.

## Demo
![alt text](demo.png)

## Motivation
Course registration often involves manually comparing different sections to avoid time conflicts and optimizing daily schedules. This project automates the process by generating conflict-free schedules.

## Features
### Version 1
- Command-line interface for schedule generation
- Automatically scrapes course data from courses.rice.edu (8 departments)
- Accepts comma-separated list of desired courses as input
- Validates course availability before processing
- Generates all valid schedules with no time conflicts
- Displays course section, CRN, instructor, and meeting times
- Option to refresh course data on each run

### Version 2
- RESTful API backend with FastAPI
- Web UI for course selection and preferences
- Automatic schedule ranking with weighted scoring algorithm
- Support for user preferences (early class penalties, gap minimization, day compactness)
- Interactive schedule visualization
- Admin endpoint for data refresh

### Version 3
- Deployed on cloud with Render
- 

## Technical Overview

### Data Layer
Course data is cached locally in `course_data.csv` (631 courses from Spring 2026). Format:

```csv
course,crn,instructor,days,start_time,end_time
COMP 140,21211,Orooji Marmar,Tue,Thu,13:00,14:15
MATH 212,21528,Radosevich Matthew,Mon,Wed,Fri,09:00,09:50
```

### V2 Architecture

**Backend:** FastAPI server with three main services:
- **Loader Service** (`app/services/loader.py`): In-memory course caching with refresh support
- **Scheduler Service** (`app/services/scheduler.py`): DFS-based conflict detection and schedule generation
- **Scorer Service** (`app/services/scorer.py`): Schedule ranking via weighted preference model

**API Endpoints:**
- `GET /api/subjects` - List all course subjects
- `GET /api/courses?query=COMP` - Search courses by name
- `POST /api/schedules` - Generate and rank schedules
  - Request: `{"courses": ["COMP 140", "MATH 212", "STAT 315"]}`
  - Response: `{"total": 10, "schedules": [[...], [...]]}`

**Frontend:** Minimal HTML form (planned: React SPA for polish)

### Scoring Algorithm
Schedules are ranked by weighted criteria:
- **Early class penalty:** -20 points if earliest class before 9:00 AM
- **Gap penalty:** -5 points per hour of gaps between classes
- **Day compactness bonus:** +30 points if all classes fit in ≤3 days
- **Future:** ILP optimization for hard constraints

### Deployment
- **Local:** `python -m uvicorn app.main:app --reload`
- **Production:** Docker + AWS (planned)

## Tech Stack
- **V1:** Python 3.11+, BeautifulSoup4, Requests
- **V2:** FastAPI, Pydantic, Python 3.11+
- **Frontend (planned):** React + Vite
- **Future:** PostgreSQL, Docker, AWS Lambda/ECS

