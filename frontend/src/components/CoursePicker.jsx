import { useState, useEffect } from 'react';

/**
 * CoursePicker.jsx - Component for browsing and searching courses
 * 
 * Props:
 *   onCourseSelect: function called when a course is selected
 */

function CoursePicker({ onCourseSelect }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch courses on component mount
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
        const response = await fetch(`${API_BASE}/api/courses`);
        if (!response.ok) throw new Error('Failed to fetch courses');
        const data = await response.json();
        // Extract just the course names from the course objects
        const courseNames = data.courses.map(c => c.course);
        setCourses(courseNames || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);

  // Filter courses based on search term
  const filteredCourses = courses.filter(course => 
    course.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Get unique course names (without section numbers)
  const uniqueCourses = [...new Set(filteredCourses)].slice(0, 50); // Limit to 50 results

  return (
    <div className="course-picker">
      <h3>Browse Courses</h3>
      
      {/* Search bar */}
      <input
        type="text"
        className="course-search"
        placeholder="Search courses (e.g., COMP 140, MATH 212)..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />

      {/* Course list */}
      <div className="course-list">
        {loading && <p className="course-list-message">Loading courses...</p>}
        {error && <p className="course-list-message error">Error: {error}</p>}
        {!loading && !error && uniqueCourses.length === 0 && (
          <p className="course-list-message">No courses found</p>
        )}
        {!loading && !error && uniqueCourses.map((course, idx) => (
          <div 
            key={idx} 
            className="course-list-item"
            onClick={() => onCourseSelect(course)}
          >
            {course}
          </div>
        ))}
      </div>
    </div>
  );
}

export default CoursePicker;
