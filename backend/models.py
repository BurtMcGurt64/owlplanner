class MeetingTime:
    """
    Contains information about when a course meets. 
        - day: a string ('Mon', 'Tue', 'Wed', etc.)
        - start: an integer representing the time the course starts, in number of minutes since midnight
        - end: an integer representing the time the course ends, in number of minutes since midnight
    """
    def __init__(self, day: str, start: int, end: int):
        """
        Initialize the MeetingTime object.
        """
        self.day = day
        self.start = start
        self.end = end

class CourseSection:
    """
    A CourseSection object represents one section of a course, identified by its CRN. 
        - Example: COMP 140, Dr. Smith, CRN 123456
    
    Each CourseSection object contains a list of MeetingTime objects, representing the times the class meets.
    """
    def __init__(self, course_name: str, crn: str, instructor: str):
        """
        Initialize the CourseSection object.
        """
        self.course_name = course_name
        self.crn = crn
        self.instructor = instructor
        self.meeting_times = []

    def add_meet_time(self, meet_time: MeetingTime):
        """
        Adds a MeetingTime object to the course.
        """
        self.meeting_times.append(meet_time)

    
    def conflicts_with(self, other) -> bool:
        """
        Checks if two courses have time conflicts. Returns True if conflict, False otherwise.
        """

        # Two times overlap if one starts before the other ends AND vice versa
        for mt1 in self.meeting_times:
            for mt2 in other.meeting_times:
                if mt1.day != mt2.day:
                    continue
                if mt1.start < mt2.end and mt2.start < mt1.end:
                    return True
                
        return False