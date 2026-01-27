/**
 * ScheduleCard.jsx - Single schedule card component
 * 
 * Props:
 *   schedule: the schedule object to display
 *   index: which schedule number this is
 *   isSelected: boolean - is this schedule currently selected
 *   onClick: function called when card is clicked
*/

function ScheduleCard({ schedule, index, isSelected, onClick }) {
  const satisfiedPrefs = schedule.satisfied_preferences || [];
  
  return (
    <div
      className={`schedule-card ${isSelected ? 'selected' : ''}`}
      onClick={onClick}
    >
      <h3>
        Schedule #{index + 1}
        {index === 0 && <span className="best-badge">BEST</span>}
      </h3>
      <p className="course-count">{schedule.courses.length} courses</p>
      
      {satisfiedPrefs.length > 0 && (
        <div className="preferences-badges">
          {satisfiedPrefs.map((pref, idx) => (
            <span key={idx} className="pref-badge">
              {pref}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export default ScheduleCard;