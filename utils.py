"""
Some helper functions.
"""

def time_to_minutes(time: str):
    """
    Helper function - 
    Given a time (e.g, "14:00"), convert that time into minutes after midnight
    """
    hours, minutes = time.split(":")
    return int(hours) * 60 + int(minutes)

def convert_to_24h(time_str: str) -> str:
    """
    Helper function to convert a given time with an AM/PM suffix into 24-hour time.
    """
    if time_str[-2:] == "AM":
        return time_str[:-2]
    else:
        time_part = time_str[:-2]
        hours, minutes = time_part.split(":")
        hours = int(hours)

        if hours != 12:
            hours += 12
        
        return f"{hours:02d}:{minutes}"