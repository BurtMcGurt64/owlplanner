from csv_parser import parse_csv, write_csv
from scheduler import generate_schedule
from web_scraper import extract_rows, get_all_subjects
import csv, os, requests

def group_by_course(sections) -> dict:
    """Groups sections by course name. Returns a dictionary where each course maps to a list of sections for that course.
    """
    courses = {}
    for sec in sections:
        if sec.course_name not in courses:
            courses[sec.course_name] = []
        courses[sec.course_name].append(sec)
    return courses

def print_schedules(schedules):
    """Prints schedules."""
    print(f"Found {len(schedules)} valid schedules\n")
    for i, schedule in enumerate(schedules[:50]):  # print first 50
        print(f"Schedule {i+1}:")
        for sec in schedule:
            times = ', '.join([f"{mt.day} {mt.start//60}:{mt.start%60:02d}-{mt.end//60}:{mt.end%60:02d}" for mt in sec.meeting_times])
            print(f"  {sec.course_name} ({sec.crn}) - {sec.instructor} - {times}")
        print()

def check_courses(desired_courses: list[str], csv_filename: str) -> tuple[list[str], list[str]]:
    """
    Given the user input desired_courses, check which courses exist in the CSV file.

    Returns a tuple in the form (found_courses, missing_courses).
    """
    # Read the CSV and extract unique course names
    existing_courses = set()
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_courses.add(row['course'])
    
    # Check which requested courses exist
    found = [c for c in desired_courses if c in existing_courses]
    missing = [c for c in desired_courses if c not in existing_courses]
    
    return found, missing

def get_user_courses() -> list[str]:
    """
    Ask the user for desired list of courses, and returns a list of the specified courses. Ex: ["COMP 140", "MATH 212"].
    """
    user_input = input("Enter courses (Ex: COMP 140, MATH 212): ")

    # Split by comma, strip whitespace
    courses = [course.strip().upper() for course in user_input.split(",")]

    return courses

def scrape_courses(filename: str, subjects: set[str]) -> int:
    """Scrape course data and write it to a CSV file."""
    all_results = []
    for subject in subjects:
        print(f"Scraping {subject}...")
        all_results.extend(extract_rows(subject))
    write_csv(all_results, filename)
    return len(all_results)

if __name__ == "__main__":
    def ask_yes_no(prompt: str) -> bool:
        answer = input(f"{prompt} [y/n]: ").strip().lower()
        return answer in {"y", "yes", ""}

    CSV_FILE = "course_data.csv"

    # Fetch all available subjects dynamically from Rice catalog
    print("GETTING RICE COURSE DATA...")
    subjects = get_all_subjects()
    
    if not subjects:
        # Fallback to default subjects if fetch fails
        print("Using default subject list (limited)...")
        subjects = {"COMP", "CMOR", "MATH", "BIOS", "CHEM", "STAT", "ECON", "FWIS", "BUSI", "MECH"}

    # scrape and write
    print(f"Will scrape {len(subjects)} subjects...")

    # check if CSV file exists, ask to scrape
    if os.path.exists(CSV_FILE):
        if ask_yes_no("Get latest Rice course data?"):
            print("Getting course data...")
            try:
                scrape_courses(CSV_FILE, subjects)
            except requests.RequestException as e:
                print(f"Error scraping courses: {e}")
                exit(1)
        else:
            print("Using existing course data.")
    else:
        print("No course data found, getting course data...")
        try:
            scrape_courses(CSV_FILE, subjects)
        except requests.RequestException as e:
            print(f"Error scraping courses: {e}")
            exit(1)
    
    # ask user for courses
    desired_courses = get_user_courses()
    if not desired_courses or desired_courses == ['']: 
        print("No courses entered. Exiting.")
        exit()

    # check courses
    try:
        found_courses, missing_courses = check_courses(desired_courses, CSV_FILE)
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found.")
        exit(1)

    if missing_courses:
        print(f"Course(s) not found: {', '.join(missing_courses)}")
    
    if not found_courses:
        print("No valid courses found.")
    else:
        # parse and generate schedules, then print
        sections = parse_csv("course_data.csv", found_courses)
        courses = group_by_course(sections)
        schedules = generate_schedule(courses)
        print_schedules(schedules)
    