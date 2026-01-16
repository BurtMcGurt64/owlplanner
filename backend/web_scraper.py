"""
This script:
    1. Fetches course data from courses.rice.edu for a given term
    2. Parses HTML table to extract course information (CRN, course name, instructor, meeting times)
    3. Converts meeting time strings (e.g., "10:00AM - 10:50AM MWF") into structured format
    4. Writes cleaned data to CSV file compatible with OwlPlanner
"""

import requests
from bs4 import BeautifulSoup
import csv
from utils import convert_to_24h, time_to_minutes

# this is the html for spring 2026 courses
url = f"https://courses.rice.edu/courses/!SWKSCAT.cat?p_action=QUERY&p_term=202620&p_subj="

# URL to fetch all available subjects
CATALOG_URL = "https://courses.rice.edu/admweb/!SWKSCAT.cat?p_action=cata"

DAY_MAP = {"M" : "Mon", "T" : "Tue", "W" : "Wed", "R" : "Thu", "F" : "Fri", "S" : "Sat", "U" : "Sun"}

def get_all_subjects() -> set[str]:
    """
    Get all available subject codes from Rice course catalog.
    
    Comprehensive list of Rice subjects extracted from the catalog.
    Last updated: Jan 2026
    
    Returns:
        - Set of subject codes like {"COMP", "MATH", "STAT", ...}
    """
    # All Rice subjects from the catalog
    RICE_SUBJECTS = {
        "AAAS", "AFSC", "AMCI", "ANTH", "APPL", "ARAB", "ARCH", "ARCR", 
        "ARTS", "ASIA", "ASTR", "BIOE", "BIOS", "BUSI", "CEVE", "CHBE", 
        "CHEM", "CHIN", "CLAS", "CLIC", "CMOR", "COLL", "COMM", "COMP", 
        "CSCI", "DSCI", "DSRT", "ECON", "EDES", "EDUC", "EEPS", "ELEC", 
        "EMBA", "EMSP", "ENGI", "ENGL", "ENST", "EURO", "FILM", "FOTO", 
        "FREN", "FWIS", "GERM", "GLBL", "GLHT", "GREE", "HART", "HEAL", 
        "HEBR", "HIST", "HONS", "HUMA", "HURC", "INDE", "INDS", "ITAL", 
        "JAPA", "JWST", "KINE", "KORE", "LALX", "LATI", "LEAD", "LING", 
        "LPAP", "LPCR", "MACC", "MATH", "MDEM", "MDHM", "MDIA", "MECH", 
        "MEOS", "MGMP", "MGMT", "MGMW", "MILI", "MSNE", "MUCH", "MUSI", 
        "NAVA", "NEUR", "NSCI", "PHIL", "PHYS", "PJHC", "PLST", "POLI", 
        "PORT", "PSYC", "RCEL", "RELI", "SMGT", "SOCI", "SOPA", "SOPE", 
        "SOSC", "SPAN", "SSPB", "STAT", "SWGS", "THEA", "TIBT", "UNIV"
    }
    
    print(f"Loaded {len(RICE_SUBJECTS)} subjects from Rice catalog")
    return RICE_SUBJECTS

def parse_meeting_strings(meeting_times: list[str]) -> list[tuple[str, str, str]]:
    """
    Given a list of meeting times represented by strings, output a list of tuples in the form (days, start_time, end_time).

    The input is of the form:
        [
            "2:00PM - 3:15PM MW  ",
            "6:30PM - 7:50 PM TR  ",
        ]

    Returns:
        List of tuples (days, start_time, end_time) where:
            - days: comma-separated day names like "Mon,Wed,Fri"
            - start_time: start time in minutes since midnight (int)
            - end_time: end time in minutes since midnight (int)
    """
    results = []

    for meet_time in meeting_times:
        if not meet_time:
            continue
        
        list_meet_time = meet_time.split(" ")

        start_raw, end_raw, days = list_meet_time[0], list_meet_time[2], list_meet_time[3]

        converted_days = []

        for day in days:
            converted_days.append(DAY_MAP[day])
        
        days_str = ",".join(converted_days)
        start_time = time_to_minutes(convert_to_24h(start_raw))
        end_time = time_to_minutes(convert_to_24h(end_raw))
        
        results.append((days_str, start_time, end_time))
    
    return results

def extract_rows(subject: str) -> list[tuple[str, str, str, str, str]]:
    """
    Extract course data for a given subject from Rice course catalog.
    
    Inputs:
        - subject: Subject code like "COMP", "MATH", etc.
    
    Returns:
        - List of tuples in the form (course_name, crn, instructor, days, start_time, end_time)
    """
    results = []
    subject_url = url + subject

    # access the url
    response = requests.get(subject_url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table')

    if not table:
        print(f"No table found for {subject}")
        return results

    # find all table rows
    rows = table.find_all('tr')
    print(f"{subject}: Found {len(rows)} courses")

    for row in rows:
        # skip header rows that contain <th>
        if row.find("th"):
            continue

        crn_cell = row.find("td", class_="cls-crn")
        course_cell = row.find("td", class_="cls-crs")
        instructor_cell = row.find("td", class_="cls-ins")
        meeting_cell = row.find("td", class_="cls-mtg")

        if not all([crn_cell, course_cell, instructor_cell, meeting_cell]):
            continue

        crn = crn_cell.get_text(strip=True)
        course_text = course_cell.get_text(" ", strip=True)

        # course_text like "MECH 200 002" -> keep subject and number
        course_parts = course_text.split()
        course_name = " ".join(course_parts[:2]) if len(course_parts) >= 2 else course_text
        instructor = instructor_cell.get_text(" ", strip=True)

        # collect meeting strings inside mtg-clas divs
        meeting_divs = []
        mtg_class = meeting_cell.find("div", class_="mtg-clas")
        if mtg_class:
            for div in mtg_class.find_all("div"):
                meeting_divs.append(div.get_text(" ", strip=True))

        for days, start, end in parse_meeting_strings(meeting_divs):
            results.append((course_name, crn, instructor, days, start, end))

    return results