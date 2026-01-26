/**
 * Empty calendar grid shown before schedules are generated
 * Copied from CalendarView
 */

function EmptyCalendarView() {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
  const startHour = 8;
  const endHour = 21; // 8 AM - 9 PM
  const hourHeight = 60; // px per hour

  return (
    <div style={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
      {/* Header row */}
      <div style={{ display: 'flex', width: '100%' }}>
        <div style={{ width: 60, flexShrink: 0 }}></div>
        {days.map(day => (
          <div 
            key={day} 
            style={{ 
              flex: 1,
              textAlign: 'center', 
              fontWeight: 'bold',
              color: '#a0aec0',
              padding: '0.5rem 0'
            }}
          >
            {day}
          </div>
        ))}
      </div>

      {/* Body */}
      <div style={{ display: 'flex', position: 'relative', width: '100%' }}>
        {/* Time labels */}
        <div style={{ width: 60, flexShrink: 0 }}>
          {Array.from({ length: endHour - startHour }, (_, i) => {
            const hour = startHour + i;
            const period = hour >= 12 ? 'PM' : 'AM';
            const displayHour = hour === 0 ? 12 : hour > 12 ? hour - 12 : hour;

            return (
              <div
                key={i}
                style={{
                  height: hourHeight,
                  whiteSpace: 'nowrap',
                  textAlign: 'right',
                  paddingRight: 4,
                  fontSize: '0.75em',
                  display: 'flex',
                  alignItems: 'flex-start',
                  paddingTop: 2,
                  color: '#718096'
                }}
              >
                {displayHour}:00 {period}
              </div>
            );
          })}
        </div>

        {/* Day columns */}
        {days.map(day => (
          <div 
            key={day} 
            style={{ 
              flex: 1,
              position: 'relative', 
              borderLeft: '1px solid #4a5568' 
            }}
          >
            {/* Hour lines */}
            {Array.from({ length: endHour - startHour }, (_, i) => (
              <div 
                key={i} 
                style={{ 
                  borderTop: '1px solid #4a5568', 
                  height: hourHeight 
                }} 
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}

export default EmptyCalendarView;
