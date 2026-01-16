"""
Implements hardcoded weights to penalize specific schedules.
"""

# default preferences, enable or disable based on user preference
DEFAULT_PREFERENCES = {
    "morning_preference": True,
    "avoid_5_days": True,
    "lunch_break": True,
    "limit_classes_per_day": True,
    "avoid_late_nights": True,
    "balance_gaps": True,
}

# Default weights (how much each category matters)
DEFAULT_WEIGHTS = {
    "morning_penalty": -5,
    "five_day_penalty": -30,
    "gap_too_short_penalty": -5,  # < 10 min
    "gap_too_long_penalty": -3,   # > 2 hours
    "lunch_bonus": +10,
    "class_count_penalty": -4,     # per class > 2 on a day
    "late_night_penalty": -10,
}

def count_unique_days(schedule: list) -> int:
    """
    Return the number of unique days in a schedule (such as 3 for Mon/Wed/Fri).

    Input:
        - schedule, a list of CourseSection objects
    """
    days = set()

    for course_section in schedule:
        for meeting in course_section.meeting_times:
            days.add(meeting.day)

    return len(days)

def earliest_start_time(schedule: list) -> int:
    """
    Returns the earliest start time in minutes.

    Input:
        - schedule, a list of CourseSection objects
    """
    earliest_time = 1440 # minutes in a day, initialize at latest possible time.

    for course_section in schedule:
        for meeting in course_section.meeting_times:
            earliest_time = min(earliest_time, meeting.start)
    
    return earliest_time

def latest_end_time(schedule: list) -> int:
    """
    Returns the latest end time in minutes.

    Input:
        - schedule, a list of CourseSection objects
    """
    latest_time = 0 # minutes in a day, initialize at earliest time

    for course_section in schedule:
        for meeting in course_section.meeting_times:
            latest_time = max(latest_time, meeting.end)
    
    return latest_time

def calculate_gaps(schedule: list) -> list:
    """
    Return list of gap durations, in minutes, between consecutive classes.
    """
    all_gaps = []
    # group schedule by day
    schedule_by_day = {"Mon" : [],
                       "Tue" : [],
                       "Wed" : [],
                       "Thu" : [],
                       "Fri" : []}

    for course_section in schedule:
        for meeting in course_section.meeting_times:
            schedule_by_day[meeting.day].append((meeting.start, meeting.end))
    
    for day, meetings in schedule_by_day.items():
        # sort by start_time
        meetings.sort()
        for i in range(len(meetings) - 1):
             # calculate the difference between end_time[i] and start_time[i+1]
            end_current = meetings[i][1]
            start_next = meetings[i+1][0]
            gap = start_next - end_current
            
            if gap > 0:
                all_gaps.append(gap)
    
    return all_gaps 

def has_lunch_break(schedule: list) -> bool:
    """
    Checks if there is a 1-hour gap that fits entirely within 11:00am - 1:00pm (660-780 minutes).
    This represents a lunch break.

    Returns True if there exists such a gap, False otherwise.
    """
    schedule_by_day = {"Mon" : [],
                       "Tue" : [],
                       "Wed" : [],
                       "Thu" : [],
                       "Fri" : []}
    
    for course_section in schedule:
        for meeting in course_section.meeting_times:
            schedule_by_day[meeting.day].append((meeting.start, meeting.end))
    
    # Check each day for lunch gap
    for meetings in schedule_by_day.values():
        if len(meetings) < 2:
            continue
        
        meetings.sort()
        
        for i in range(len(meetings) - 1):
            end_current = meetings[i][1]
            start_next = meetings[i+1][0]
            gap = start_next - end_current
            
            # Calculate how much of the gap overlaps with lunch window (11am-1pm, 660-780 minutes)
            if gap >= 60:
                overlap_start = max(end_current, 660)
                overlap_end = min(start_next, 780)
                overlap_duration = overlap_end - overlap_start
                
                # If at least 60 minutes overlap with lunch window
                if overlap_duration >= 60:
                    return True
    
    return False

def classes_per_day(schedule: list) -> dict:
    """
    Check the number of classes per day. Returns a dict where each key represents the day, mapping to the frequency to which that day appears.
    """
    day_freq = {"Mon" : 0,
                "Tue" : 0,
                "Wed" : 0,
                "Thu" : 0,
                "Fri" : 0}
    
    for course_section in schedule:
        for meeting in course_section.meeting_times:
            day_freq[meeting.day] += 1
    
    return day_freq

def score_schedule(schedule: list, preferences: dict = None, weights: dict = None) -> float:
    """
    Score a schedule based on preferences and weights.

    Inputs:
        - schedule: a list of CourseSection objects
        - preferences: dictionary of enabled categories (use DEFAULT_PREFERENCES if None)
        - weights: dict of penalty and bonus values (use DEFAULT_WEIGTHS if None)
    
    Returns:
        - float: the total score. A higher score is a better schedule.
    """
    score = 0.0

    # merge the user preferences with defaults
    prefs = {**DEFAULT_PREFERENCES, **(preferences or {})}
    wts = {**DEFAULT_WEIGHTS, **(weights or {})}

    # AVOID 5 DAY WEEKS
    if prefs["avoid_5_days"]:
        days = count_unique_days(schedule)
        if days >= 5:
            score += wts["five_day_penalty"]
    
    # MORNING PREFERENCE
    if prefs["morning_preference"]:
        earliest = earliest_start_time(schedule)
        if earliest < 540:  # before 9am
            score += wts["morning_penalty"]
    
    # AVOID LATE NIGHTS
    if prefs["avoid_late_nights"]:
        latest = latest_end_time(schedule)
        if latest > 1140:  # after 7pm
            score += wts["late_night_penalty"]
    
    # BALANCE GAPS (no rushing between classes/wasted time)
    if prefs["balance_gaps"]:
        gaps = calculate_gaps(schedule)
        for gap_mins in gaps:
            if gap_mins < 10:  # rushing between classes
                score += wts["gap_too_short_penalty"]
            elif gap_mins > 120:  # too much idle time
                score += wts["gap_too_long_penalty"]
    
    # LUNCH
    if prefs["lunch_break"] and has_lunch_break(schedule):
        score += wts["lunch_bonus"]

    # MORE THAN 3 CLASSES PER DAY
    if prefs["limit_classes_per_day"]:
        per_day = classes_per_day(schedule)
        for day, count in per_day.items():
            if count >= 3:
                score += wts["class_count_penalty"] * (count - 2)  # penalty per extra class
    
    return score

def get_satisfied_preferences(schedule: list, preferences: dict = None) -> list:
    """
    Returns a list of preference names that this schedule satisfies.
    
    Inputs:
        - schedule: a list of CourseSection objects
        - preferences: dictionary of enabled categories (use DEFAULT_PREFERENCES if None)
    
    Returns:
        - list of strings: names of satisfied preferences
    """
    satisfied = []
    prefs = {**DEFAULT_PREFERENCES, **(preferences or {})}
    
    # Check if avoids 5-day week
    if prefs["avoid_5_days"]:
        days = count_unique_days(schedule)
        if days < 5:
            satisfied.append("4-Day Week")
    
    # Check if no early mornings
    if prefs["morning_preference"]:
        earliest = earliest_start_time(schedule)
        if earliest >= 540:  # 9am or later
            satisfied.append("No Early Classes (before 9 AM)")
    
    # Check if no late nights
    if prefs["avoid_late_nights"]:
        latest = latest_end_time(schedule)
        if latest <= 1140:  # before 7pm
            satisfied.append("No Late Classes")
    
    # Check for balanced gaps
    if prefs["balance_gaps"]:
        gaps = calculate_gaps(schedule)
        # Only show badge if there are gaps and none are bad
        if gaps and not any(gap < 10 or gap > 120 for gap in gaps):
            satisfied.append("Balanced Gaps")
        # If there are no gaps at all (back-to-back classes), also show as balanced
        elif not gaps:
            satisfied.append("Balanced Gaps")
    
    # Check for lunch break
    if prefs["lunch_break"] and has_lunch_break(schedule):
        satisfied.append("Lunch Break (1 hour)")
    
    # Check for reasonable class count per day
    if prefs["limit_classes_per_day"]:
        per_day = classes_per_day(schedule)
        max_per_day = max(per_day.values()) if per_day else 0
        if max_per_day <= 2:
            satisfied.append("Max 2 Classes/Day")
    
    return satisfied