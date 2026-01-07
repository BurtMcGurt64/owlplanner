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
- Web GUI with FastAPI backend and React frontend
- Supports user preferences (avoid early classes, minimize gaps, etc.)
- Scores and ranks schedules based on weighted criteria
- Interactive schedule visualization

## Technical Overview
### Data
Course data is automatically scraped from courses.rice.edu for Spring 2026. The data is cached locally in `course_data.csv` with the format:

```csv
course,crn,instructor,days,start_time,end_time
COMP 140,12345,Smith,Mon,Wed,10:00,11:15
MATH 212,23456,Johnson,Tue,Thu,13:00,14:15
```

## Tech Stack
- **V1:** Python 3.11+, BeautifulSoup4, Requests
- **V2 (Planned):** FastAPI, React

