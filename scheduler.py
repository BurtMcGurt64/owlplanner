from models import CourseSection

def generate_schedule(courses: dict[str, list[CourseSection]]) -> list[list[CourseSection]]:
    """
    Generates a valid set of schedules given a selection of courses.

    Input:
        - courses, a dictionary where each course name maps to a list of sections, represented by CourseSection objects, corresponding to that course. Example:
            {
                "COMP 140": [sec_A, sec_B, sec_C],
                "MATH 212": [sec_D, sec_E],
            }

    Output:
        - schedule, a list of lists, where each inner list represents one complete schedule.
    """

    course_names = list(courses.keys())
    schedules = []

    # we will use recursive dfs here to generate all schedules
    # skip to the next section when there is a time conflict
    def dfs(idx: int, current_schedule: list[CourseSection]):
        """
        Appends valid schedules to the list schedules, recursively.

        Input:
            - idx, an integer representing the index of the current course for which we are picking a section for.
            - current_schedule, a list of CourseSection objects, representing the courses chosen so far at the depth. 
        """

        # base case: if all courses have been chosen
        if idx == len(course_names):
            schedules.append(current_schedule.copy())
            return
        
        course_name = course_names[idx]

        for section in courses[course_name]:
            # check for conflicts
            conflict = False
            for scheduled_course in current_schedule:
                if section.conflicts_with(scheduled_course):
                    conflict = True
                    break
            
            if conflict:
                continue
        
            current_schedule.append(section)

            # build the rest of the schedule
            dfs(idx + 1, current_schedule)

            current_schedule.pop()

    dfs(0, [])

    return schedules


