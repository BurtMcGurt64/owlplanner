# Project Idea:
This is a schedule optimizer for courses at Rice University. Given a selection of courses for the semester, it will determine the best and most optimal schedules for those courses. 

## Key Features - Version 1
* Input: A list of courses the student wants to take, in CSV format
* Output: A list of all valid schedules with no time conflicts
* Each schedule shows the section of that course, the course request number (CRN), professor, and meeting times
* Data will be taken from Rice's Esther course website for the semester
* There will be a simple UI (minimal web form)

## Add-On Features - Version 2
* Users can specify preferences:
    * Avoid classes before 9am
    * Minimize gaps between classes
    * Preference for certain days
    * Minimize walking distance
* The system will rank and score the 'best' schedules given those preferences

# Future Add-Ons
* Prerequisite checking (warns if you're missing prereqs)
* Major requirements tracker
* Web interface
* Include course/instructor evaluations into the weightings
* Distribution requirements