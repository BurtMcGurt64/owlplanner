import { useState } from 'react';
import ScheduleCard from './ScheduleCard';
import CalendarView from './CalendarView';

/**
 * ScheduleList.jsx - Displays list of generated schedules
 * 
 * Props:
 *   schedules: array of schedule objects from API
 *   total: total number of valid schedules found (before pagination)
 * 
 * This component:
 * 1. Shows a list of schedule cards
 * 2. Lets user click to select one
 * 3. Displays details of selected schedule
 */

function ScheduleList({ schedules, total }) {
  // TODO: Track which schedule the user selected
  const [selectedIdx, setSelectedIdx] = useState(0);
  
  // Don't render if no schedules
  if (!schedules || schedules.length === 0) {
    return null;
  }

  const selectedSchedule = schedules[selectedIdx];
  
  // DEBUG
  console.log('All schedules:', schedules);
  console.log('Selected schedule:', selectedSchedule);
  console.log('Courses in selected schedule:', selectedSchedule.courses);

  return (
    <div className="schedule-list">
      <h2 className="schedule-list-title">
        Your schedules
        {total > schedules.length && ` (showing top ${schedules.length} of ${total})`}
      </h2>
      
      <div className="schedule-container">
        {/* Left side - List of schedule cards */}
        <div className="schedule-cards">
          {schedules.map((schedule, idx) => (
            <ScheduleCard
              key={idx}
              schedule={schedule}
              index={idx}
              isSelected={selectedIdx === idx}
              onClick={() => setSelectedIdx(idx)}
            />
          ))}
        </div>

        {/* Right side - Calendar view */}
        <div className="schedule-details">
          <CalendarView schedule={selectedSchedule} />
        </div>
      </div>
    </div>
  );
}

export default ScheduleList;
