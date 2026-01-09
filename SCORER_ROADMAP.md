# Scorer.py Implementation Roadmap

## Goal
Build `app/services/scorer.py` with a `score_schedule()` function that ranks schedules based on preferences and weights.

---

## Step 1: Define Constants (5 mins)
Create module-level defaults at the top of `scorer.py`:

```python
# Default preferences (enable/disable categories)
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
```

---

## Step 2: Build Helper Functions (20 mins)

Write these utility functions that `score_schedule()` will use. Each takes a `schedule` (list of CourseSection objects) and returns a value:

### 2.1 Count unique days
```python
def count_unique_days(schedule: list) -> int:
    """Return number of unique days in schedule (e.g., 3 for Mon/Wed/Fri)"""
    # Hint: iterate through schedule, collect unique day values
```

### 2.2 Find earliest/latest times
```python
def earliest_start_time(schedule: list) -> int:
    """Return earliest start time in minutes (e.g., 540 for 9:00am)"""

def latest_end_time(schedule: list) -> int:
    """Return latest end time in minutes (e.g., 1140 for 7:00pm)"""
```

### 2.3 Calculate gaps between classes
```python
def calculate_gaps(schedule: list) -> list:
    """
    Return list of gap durations (in minutes) between consecutive classes.
    
    Example: If COMP 140 ends at 2:00pm and MATH 212 starts at 3:00pm, gap = 60 mins
    
    Hint:
    1. Group schedule by day
    2. For each day, sort by start_time
    3. Calculate difference between end_time[i] and start_time[i+1]
    4. Return all gaps as a list
    """
```

### 2.4 Check for lunch break
```python
def has_lunch_break(schedule: list) -> bool:
    """
    Return True if there's a 1-hour gap between 11:30am-1:30pm (690-810 minutes).
    This indicates a lunch opportunity.
    
    Hint: Use calculate_gaps(), check if any gap falls in that time window
    """
```

### 2.5 Count classes per day
```python
def classes_per_day(schedule: list) -> dict:
    """
    Return dict like {"Mon": 2, "Tue": 1, "Wed": 2, ...}
    
    Hint: Iterate through schedule, count occurrences of each day
    """
```

---

## Step 3: Implement Main Scoring Function (15 mins)

```python
def score_schedule(
    schedule: list,
    preferences: dict = None,
    weights: dict = None
) -> float:
    """
    Score a schedule based on preferences and weights.
    
    Args:
        schedule: List of CourseSection objects
        preferences: Dict of enabled categories (optional, use DEFAULT_PREFERENCES if None)
        weights: Dict of penalty/bonus values (optional, use DEFAULT_WEIGHTS if None)
    
    Returns:
        float: Total score (higher is better)
    """
    
    # Step 1: Merge user overrides with defaults
    prefs = {**DEFAULT_PREFERENCES, **(preferences or {})}
    wts = {**DEFAULT_WEIGHTS, **(weights or {})}
    
    # Step 2: Initialize score
    score = 0.0
    
    # Step 3: Apply scoring rules (if enabled in prefs)
    
    # Rule 1: Avoid 5+ day weeks
    if prefs["avoid_5_days"]:
        days = count_unique_days(schedule)
        if days >= 5:
            score += wts["five_day_penalty"]  # negative value
    
    # Rule 2: Morning preference
    if prefs["morning_preference"]:
        earliest = earliest_start_time(schedule)
        if earliest < 540:  # before 9am
            score += wts["morning_penalty"]
    
    # Rule 3: Avoid late nights
    if prefs["avoid_late_nights"]:
        latest = latest_end_time(schedule)
        if latest > 1140:  # after 7pm
            score += wts["late_night_penalty"]
    
    # Rule 4: Balance gaps (no rushing, no wasted time)
    if prefs["balance_gaps"]:
        gaps = calculate_gaps(schedule)
        for gap_mins in gaps:
            if gap_mins < 10:  # rushing between classes
                score += wts["gap_too_short_penalty"]
            elif gap_mins > 120:  # too much idle time
                score += wts["gap_too_long_penalty"]
    
    # Rule 5: Lunch bonus
    if prefs["lunch_break"] and has_lunch_break(schedule):
        score += wts["lunch_bonus"]
    
    # Rule 6: Limit classes per day (penalize if 3+ classes on any day)
    if prefs["limit_classes_per_day"]:
        per_day = classes_per_day(schedule)
        for day, count in per_day.items():
            if count >= 3:
                score += wts["class_count_penalty"] * (count - 2)  # penalty per extra class
    
    # Step 4: Return final score
    return score
```

---

## Step 4: Testing Checklist (10 mins)

Before moving to integration, test these in Python:

```python
from app.services.scorer import score_schedule, calculate_gaps, classes_per_day

# Test 1: Load some schedules and score them
schedules = [...]  # from your test data
scores = [score_schedule(s) for s in schedules]
print(scores)

# Test 2: Verify gaps calculation
schedule = [...]
gaps = calculate_gaps(schedule)
print(gaps)

# Test 3: Custom preferences
custom_prefs = {"morning_preference": False, "avoid_5_days": True}
score = score_schedule(schedule, preferences=custom_prefs)
print(score)

# Test 4: Custom weights
custom_weights = {"morning_penalty": -100}  # heavily penalize early
score = score_schedule(schedule, weights=custom_weights)
print(score)
```

---

## Implementation Tips

1. **Time math:** Remember times in your CSV are strings like `"13:00"`. You'll need to convert to minutes: `int(hours) * 60 + int(minutes)`.

2. **CourseSection objects:** They have `meeting_times` which is a list. Each has `.day`, `.start`, `.end` (already in minutes).

3. **Sorting days:** When grouping by day, remember order: `["Mon", "Tue", "Wed", "Thu", "Fri"]` (not alphabetical).

4. **Edge cases:**
   - Empty schedule (shouldn't happen, but handle gracefully)
   - Single course (no gaps)
   - Schedules with only one day

5. **Return types:** Keep everything as `float` so sorting works smoothly.

---

## File Structure

```
app/services/scorer.py
├── DEFAULT_PREFERENCES
├── DEFAULT_WEIGHTS
├── count_unique_days()
├── earliest_start_time()
├── latest_end_time()
├── calculate_gaps()
├── has_lunch_break()
├── classes_per_day()
└── score_schedule()  [main function]
```

---

## Success Criteria

✅ `score_schedule()` accepts optional preferences and weights  
✅ Higher score = better schedule  
✅ Schedules can be sorted by score  
✅ Works with empty/None preferences/weights (uses defaults)  
✅ No crashes on edge cases (1 course, etc.)  

**Estimated time: 45 mins total**

---

## Next Steps (After You Finish)

1. Integrate into `app/routers/schedules.py` (sort by score before returning)
2. Test on `/docs` API
3. Add preferences endpoint (allow users to customize)
