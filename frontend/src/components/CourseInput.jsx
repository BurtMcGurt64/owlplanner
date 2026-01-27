import { useState } from 'react';

/**
 * CourseInput.jsx - Form for entering courses
 * 
 * Props:
 *   onGenerate: function called when form is submitted with courses array
 *   isLoading: boolean - if true, disable the input (we're waiting for API)
 * 
 * This component:
 * 1. Has its own local state (courseText) for the textarea
 * 2. Validates the input
 * 3. Calls onGenerate with the parsed course list
 */

function CourseInput({ onGenerate, isLoading }) {
  const [courseText, setCourseText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Parse courses from textarea
    const courses = courseText
      .split(',')
      .map(c => c.trim())
      .filter(c => c)
      .map(c => {
        // Normalize: uppercase, remove extra whitespace
        return c.toUpperCase().replace(/\s+/g, ' ');
      });
    
    if (courses.length === 0) {
      return;
    }
    
    // Call parent component's function with the courses
    onGenerate(courses);
  };

  return (
    <form onSubmit={handleSubmit} className="course-input-form">
      <div>
        <label htmlFor="courses" className="form-label">
          Enter Courses (comma-separated):
        </label>
        
        <textarea
          id="courses"
          value={courseText}
          onChange={(e) => setCourseText(e.target.value)}
          placeholder="e.g., COMP 140, MATH 212, STAT 315"
          className="form-input"
          disabled={isLoading}
          rows="3"
        />
      </div>
      
      <button
        type="submit"
        disabled={isLoading}
        className="btn btn-primary"
      >
        {isLoading ? 'Generating...' : 'Generate Schedules'}
      </button>
    </form>
  );
}``

export default CourseInput;
