/**
 * PreferenceSelector.jsx - Component for selecting scheduling preferences
 * 
 * Props:
 *   preferences: object with boolean values for each preference
 *   onPreferencesChange: function called when any preference changes
 */

function PreferenceSelector({ preferences, onPreferencesChange }) {
  const handleToggle = (key) => {
    onPreferencesChange({
      ...preferences,
      [key]: !preferences[key],
    });
  };

  return (
    <div className="preference-selector">
      <h3 className="preference-title">Scheduling Preferences</h3>
      <div className="preference-grid">
        <label className="preference-item">
          <input
            type="checkbox"
            checked={preferences.morning_preference}
            onChange={() => handleToggle('morning_preference')}
          />
          <span>No classes before 9 AM</span>
        </label>

        <label className="preference-item">
          <input
            type="checkbox"
            checked={preferences.avoid_5_days}
            onChange={() => handleToggle('avoid_5_days')}
          />
          <span>Prefer 4-day week</span>
        </label>

        <label className="preference-item">
          <input
            type="checkbox"
            checked={preferences.lunch_break}
            onChange={() => handleToggle('lunch_break')}
          />
          <span>1-hour lunch break (11 AM–1 PM)</span>
        </label>

        <label className="preference-item">
          <input
            type="checkbox"
            checked={preferences.limit_classes_per_day}
            onChange={() => handleToggle('limit_classes_per_day')}
          />
          <span>Max 2 classes per day</span>
        </label>

        <label className="preference-item">
          <input
            type="checkbox"
            checked={preferences.avoid_late_nights}
            onChange={() => handleToggle('avoid_late_nights')}
          />
          <span>No classes after 7 PM</span>
        </label>

        <label className="preference-item">
          <input
            type="checkbox"
            checked={preferences.balance_gaps}
            onChange={() => handleToggle('balance_gaps')}
          />
          <span>Balanced gaps between classes</span>
        </label>
      </div>
    </div>
  );
}

export default PreferenceSelector;
