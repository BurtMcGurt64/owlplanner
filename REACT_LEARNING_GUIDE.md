# React Learning Guide - Build OwlPlanner Step by Step

Welcome! You're rebuilding the frontend from scratch to actually understand what's happening. This document guides you through the learning process.

## Key React Concepts You'll Learn

### 1. **Components** 
- Reusable pieces of the UI
- Think of them like functions that return JSX (HTML-like syntax)
- In React, everything is a component

### 2. **Props** (like function parameters)
- Data passed FROM parent → child component
- Read-only (child can't change them)
- Example: `<CourseInput onGenerate={handleGenerate} />`
  - `onGenerate` is a prop

### 3. **State** (like component memory)
- Data that can change
- Managed with `useState` hook
- When state changes, component re-renders with new data
- Example: `const [courseText, setCourseText] = useState('')`

### 4. **Data Flow** (One-way street)
```
App.jsx (parent)
  ↓ sends props down ↓
CourseInput.jsx (child)
  ↓ user types ↓
  ↓ form submitted ↓
  ↓ calls callback function (onGenerate) ↑
App.jsx gets the data back
```

---

## Building Steps (Follow in Order!)

### **Step 0: Understand the API (Review Only)**
📄 Look at `frontend/src/api.js`

This file talks to your backend. Just read it—don't change it.
```javascript
// It does one thing: takes a list of courses, sends them to backend
// and returns schedules
export async function fetchSchedules(courses) { ... }
```

**Key points:**
- `async` = this takes time (API call is slow)
- `await` = wait for the response
- URL comes from `.env` file

---

### **Step 1: Build CourseInput Component**
📄 File: `frontend/src/components/CourseInput.jsx`

**What it does:**
1. Shows a textarea for entering courses
2. Has a button to submit
3. Validates input (at least 1 course)
4. Calls the parent's `onGenerate()` callback with the courses

**Todo checklist:**
- [ ] Read and understand the existing code (has TODOs in comments)
- [ ] Try running it. Type some courses and click the button
- [ ] Open browser dev tools (F12) → Console
- [ ] You should see "Please enter at least one course" alert work
- [ ] Try typing "COMP 140, MATH 212" and clicking button

**Questions to ask yourself:**
- What does `e.preventDefault()` do? (Hint: stops page reload)
- What does `.split(',')` do? (Splits string by comma)
- What does `.trim()` do? (Removes whitespace)

---

### **Step 2: Build App Component (Parent)**
📄 File: `frontend/src/App.jsx`

**What it does:**
1. Manages the main state (schedules, loading, error)
2. Calls the API when user submits courses
3. Passes data DOWN to child components

**Key concept: useState**
```javascript
const [schedules, setSchedules] = useState(null);
// schedules = current value
// setSchedules = function to change it
// null = starting value
```

**Todo checklist:**
- [ ] Read the code and TODOs
- [ ] Go test: Type courses in the input, click button
- [ ] Watch for loading spinner to appear
- [ ] In console, you should see API calls being made
- [ ] If API works, you should see schedules appear!

**Don't worry if the styling looks off yet—we're fixing that next.**

---

### **Step 3: Build ScheduleList Component**
📄 File: `frontend/src/components/ScheduleList.jsx`

**What it does:**
1. Shows a list of schedule cards (left side)
2. Lets user click to select one
3. Shows details of selected schedule (right side)

**Key concept: Props and State**
- Gets `schedules` and `total` from parent (App.jsx) as PROPS
- Has its own state `selectedIdx` to track which one is selected

**Todo checklist:**
- [ ] Read the code
- [ ] Generate some schedules
- [ ] Click on different schedule cards
- [ ] See the selected one highlighted
- [ ] The right side should show the selected schedule number

---

### **Step 4: Build ScheduleCard Component** 
📄 File: `frontend/src/components/ScheduleCard.jsx`

**What it does:**
- Displays ONE schedule card
- Very simple component (no state, just props)

**Key concept: "Dumb" Components**
- Receives data as props
- Just displays it
- Parent handles all the logic

**Todo checklist:**
- [ ] Already done! Read the code (it's simple)
- [ ] See how it gets data as props from ScheduleList

---

### **Step 5: Style Everything**
📄 File: `frontend/src/App.css`

**Already done!** The CSS is organized and clean.

**How it works:**
- Components use `className="class-name"` 
- CSS file has styles for each class
- Much better than inline styles!

**Example:**
```javascript
// In component
<button className="btn btn-primary">Click me</button>

// In CSS
.btn-primary {
  background-color: #667eea;
  color: white;
}
```

---

## Current Status

✅ **Done:**
- App component with state management
- CourseInput component
- ScheduleList component (simplified)
- ScheduleCard component
- Organized CSS file
- API integration ready

**Next TODO items in the code:**
- In `CourseInput`: Review the form logic (comment says "TODO: Handle form submission")
- In `App`: Review state management (comment says "TODO: Learn about useState")
- In `ScheduleList`: Add calendar view (once API returns more data)

---

## How to Run It

```bash
cd /Users/eddie/Projects/schedule_optimizer/frontend
npm run dev
```

Then open http://localhost:5173 in your browser.

---

## Testing Checklist

**Test 1: Empty Input**
- Click "Generate" without typing anything
- Should show alert "Please enter at least one course"

**Test 2: One Course**
- Type "COMP 140"
- Click "Generate"
- Should show loading spinner
- Should see results when API responds

**Test 3: Multiple Courses**
- Type "COMP 140, MATH 212, STAT 315"
- Click "Generate"
- Should show all matching schedules

**Test 4: Select Schedules**
- Generate schedules
- Click different cards
- Right side should update

---

## JavaScript/React Concepts Explained

### useState - Component Memory
```javascript
const [value, setValue] = useState(startValue);
```
- `value` = current data
- `setValue` = function to change it
- React re-renders whenever you call setValue
- Must import: `import { useState } from 'react'`

### Props - Parent to Child
```javascript
// Parent (App)
<CourseInput onGenerate={handleGenerate} />

// Child (CourseInput)
function CourseInput({ onGenerate }) {
  // Can use onGenerate as a function
  onGenerate(['COMP 140']);
}
```

### Conditional Rendering - Show/Hide
```javascript
// Show loading only if loading
{isLoading && <div>Loading...</div>}

// Show error only if error exists
{error && <div>{error}</div>}

// Show results only if we have them
{schedules && <ScheduleList schedules={schedules} />}
```

### Array Methods
```javascript
const courses = "COMP 140, MATH 212".split(',');
// courses = ["COMP 140", " MATH 212"]

const trimmed = courses.map(c => c.trim());
// trimmed = ["COMP 140", "MATH 212"]

const filtered = trimmed.filter(c => c);
// filtered = ["COMP 140", "MATH 212"] (removes empty strings)

// Or chain them:
const result = courseText.split(',').map(c => c.trim()).filter(c => c);
```

### Rendering Lists
```javascript
{schedules.map((schedule, idx) => (
  <ScheduleCard 
    key={idx}  // React needs this for list rendering
    schedule={schedule}  // Pass as prop
    index={idx}
  />
))}
```

---

## Common Mistakes to Avoid

❌ **Don't mutate state directly**
```javascript
// WRONG
state.value = newValue;

// RIGHT
setState(newValue);
```

❌ **Don't forget parentheses on functions**
```javascript
// WRONG
<button onClick={handleClick}>  // Calls immediately on render!

// RIGHT
<button onClick={() => handleClick()}>
// or
<button onClick={handleClick}>  // If no params needed
```

❌ **Don't forget `key` in lists**
```javascript
// WRONG
{items.map(item => <div>{item}</div>)}

// RIGHT
{items.map((item, idx) => <div key={idx}>{item}</div>)}
```

---

## Next Steps After This

Once this works and you understand it:

1. **Add course search typeahead** - fetch courses from API as you type
2. **Add course chips** - show selected courses as removable chips
3. **Add calendar view** - visualize the schedule on a calendar
4. **Add preferences** - let users set preferences (once backend supports it)
5. **Add export** - export schedule to Google Calendar

---

## Getting Help

When something breaks:
1. Check the browser console (F12 → Console)
2. Read the error message carefully
3. Check that all files are saved
4. Restart the dev server (`Ctrl+C`, then `npm run dev` again)
5. Make sure the backend is running

---

**Happy coding! You've got this! 🚀**
