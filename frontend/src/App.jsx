import { useEffect, useState } from 'react';
import './App.css';
import CourseInput from './components/CourseInput';
import PreferenceSelector from './components/PreferenceSelector';
import ScheduleList from './components/ScheduleList';
import { fetchSchedules, pingHealth } from './api';

/**
 * App.jsx - Main component that manages the app state and layout
 * 
 * 1. Manages all the state (data that changes)
 * 2. Handles API calls
 * 3. Passes data DOWN to child components (via props)
 * 4. Receives events UP from child components (via callbacks)
 */

function App() {
  // Backend warmup state
  const [backendReady, setBackendReady] = useState(false);
  const [warmingUp, setWarmingUp] = useState(true);
  
  // Warm the backend on first load to avoid cold-start delay
  useEffect(() => {
    const warmupBackend = async () => {
      setWarmingUp(true);
      // Try multiple times with increasing timeout
      for (let attempt = 0; attempt < 3; attempt++) {
        const ready = await pingHealth(30000); // 30s per attempt
        if (ready) {
          setBackendReady(true);
          setWarmingUp(false);
          return;
        }
      }
      // After 3 attempts, give up but let user try anyway
      setWarmingUp(false);
      setBackendReady(false);
    };
    warmupBackend();
  }, []);
  
  // These store the schedule results from the API
  const [schedules, setSchedules] = useState(null);
  const [total, setTotal] = useState(0);
  
  // These manage UI state (loading spinner, error messages)
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // User preferences for scheduling
  const [preferences, setPreferences] = useState({
    morning_preference: true,
    avoid_5_days: true,
    lunch_break: true,
    limit_classes_per_day: true,
    avoid_late_nights: true,
    balance_gaps: true,
  });

  const handleGenerate = async (courses) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // API call to backend with preferences
      const data = await fetchSchedules(courses, preferences);
      setSchedules(data.schedules);
      setTotal(data.total);
    } catch (err) {
      setError(err.message);
      setSchedules(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1>🦉 OwlPlanner</h1>
        <p>Course Scheduler for Rice University</p>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Backend warmup banner */}
        {warmingUp && (
          <div className="info-box" style={{ backgroundColor: '#fff3cd', borderColor: '#ffc107' }}>
            <strong> Waking up backend...</strong> This takes ~30 seconds on first visit.
          </div>
        )}
        
        {/* Preference Selector */}
        <PreferenceSelector 
          preferences={preferences} 
          onPreferencesChange={setPreferences} 
        />

        {/* Course Input Form */}
        <CourseInput 
          onGenerate={handleGenerate} 
          isLoading={isLoading || warmingUp} 
        />

        {/* Error Message */}
        {error && (
          <div className="error-box">
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Loading Spinner */}
        {isLoading && (
          <div className="loading">
            <div className="spinner">⏳</div>
            <p>Generating schedules...</p>
          </div>
        )}

        {/* Schedule Results */}
        {schedules && !isLoading && (
          <ScheduleList schedules={schedules} total={total} />
        )}
      </main>
    </div>
  );
}

export default App;
