/**
 * CalendarView.jsx - Visual calendar of the schedule
 * 
 * Uses 30-minute time slots and fractional rows for accurate positioning
 */

function CalendarView({ schedule }) {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
  const startHour = 8;
  const endHour = 21; // 8 AM - 9 PM
  const dayColumnWidth = 120; // px
  const hourHeight = 60; // px per hour
  const minutesPerPixel = hourHeight / 60; // scale for top/height

  const colors = ['#667eea', '#f56565', '#48bb78', '#ed8936', '#9f7aea', '#38b2ac'];

  const formatTime = (minutes) => {
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    const period = h >= 12 ? 'PM' : 'AM';
    const displayHour = h > 12 ? h - 12 : h === 0 ? 12 : h;
    return `${displayHour}:${m.toString().padStart(2, '0')} ${period}`;
  };

  // Organize courses by day
  const coursesByDay = {};
  days.forEach(day => coursesByDay[day] = []);
  schedule.courses.forEach((course, idx) => {
    course.meeting_times.forEach(mt => {
      if (coursesByDay[mt.day]) {
        coursesByDay[mt.day].push({
          ...course,
          start: mt.start,
          end: mt.end,
          colorIdx: idx % colors.length
        });
      }
    });
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      {/* Header row */}
      <div style={{ display: 'flex' }}>
        <div style={{ width: 60 }}></div>
        {days.map(day => (
          <div key={day} style={{ width: dayColumnWidth, textAlign: 'center', fontWeight: 'bold' }}>{day}</div>
        ))}
      </div>

      {/* Body */}
      <div style={{ display: 'flex', position: 'relative' }}>
        {/* Time labels */}
        <div style={{ width: 60 }}>
        {Array.from({ length: endHour - startHour }, (_, i) => {
            const hour = startHour + i;
            const period = hour >= 12 ? 'PM' : 'AM';
            const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;

            return (
            <div
                key={i}
                style={{
                height: hourHeight,
                whiteSpace: 'nowrap',   // prevent AM/PM wrapping
                textAlign: 'right',     // align to the right edge
                paddingRight: 4,
                fontSize: '0.75em',
                display: 'flex',
                alignItems: 'flex-start',  // align text to top of the row
                paddingTop: 2              // small padding from top
                }}
            >
                {displayHour}:00 {period}
            </div>
            );
        })}
        </div>

        {/* Day columns */}
        {days.map(day => (
          <div key={day} style={{ width: dayColumnWidth, position: 'relative', borderLeft: '1px solid #eeeeee2d' }}>
            {/* Hour lines */}
            {Array.from({ length: endHour - startHour }, (_, i) => (
              <div key={i} style={{ borderTop: '1px solid #eeeeee2d', height: hourHeight }} />
            ))}

            {/* Courses */}
            {coursesByDay[day].map((course, idx) => {
              const top = (course.start - startHour * 60) * minutesPerPixel;
              const height = (course.end - course.start) * minutesPerPixel;

              return (
                <div
                  key={idx}
                  style={{
                    position: 'absolute',
                    top,
                    left: 2,
                    right: 2,
                    height,
                    backgroundColor: colors[course.colorIdx],
                    borderRadius: 4,
                    padding: '2px',
                    color: 'white',
                    fontSize: '0.75em',
                    overflow: 'hidden'
                  }}
                >
                  <div>{course.course}</div>
                  <div style={{ fontSize: '0.7em' }}>{formatTime(course.start)} - {formatTime(course.end)}</div>
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

export default CalendarView;

