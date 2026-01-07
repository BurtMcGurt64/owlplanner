""" Parses the CSV data """
import csv
from models import CourseSection, MeetingTime
from utils import time_to_minutes

def parse_csv(filename, course_names: list[str] | None = None):
    """
    Given a CSV file, return a list of CourseSection objects.

    If course_names is provided (in the form ["COURSE 1", "COURSE 2"]), only parse those courses.

    If course_names is None, parse all courses in the CSV file.
    """

    # group courses with same name in a dictionary
    # keys are CRNs and values are CourseSection objects
    sections = {}

    with open(filename) as file:
        reader = csv.DictReader(file)

        for row in reader:
            # extract information from row
            course_name = row['course']
            crn = row['crn']
            instructor = row['instructor']
            days = row['days']
            start_time = row['start_time']
            end_time = row['end_time']

            # before creating the CourseSection object, check:
            if course_names is not None and course_name not in course_names:
                continue # skip the row

            # create a new CourseSection object
            new_course = CourseSection(course_name, crn, instructor)

            # separate the days column
            list_days = days.split(",")
            for day in list_days:
                # add new meeting time to the CourseSection object
                new_course.add_meet_time(
                    MeetingTime(day, time_to_minutes(start_time),
                                time_to_minutes(end_time)))


            # add course to the dictionary
            sections[crn] = new_course

    # return a list of all courses
    return list(sections.values())

def write_csv(all_results: list[tuple], filename: str = "course_data.csv"):
    """
    Write course data to CSV file.

    Input:
        - all_results: list of tuples in the form (course, crn, instructor, days, start_mins, end_mins)
        - filename: the name of the CSV file to write data into
    """

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['course', 'crn', 'instructor', 'days', 'start_time', 'end_time'])

        for course, crn, instructor, days, start, end in all_results:
            # Convert minutes back to HH:MM format
            start_str = f"{start//60:02d}:{start%60:02d}"
            end_str = f"{end//60:02d}:{end%60:02d}"
            writer.writerow([course, crn, instructor, days, start_str, end_str])
    
    print(f"Added {len(all_results)} course meetings to {filename}")