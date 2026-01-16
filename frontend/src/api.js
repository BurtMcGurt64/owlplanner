// API helper functions
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

export async function fetchSchedules(courses, preferences = null) {
  console.log('Calling API:', `${API_BASE}/api/schedules`);
  console.log('With courses:', courses);
  console.log('With preferences:', preferences);

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 20000); // 20s timeout
  
  try {
    const res = await fetch(`${API_BASE}/api/schedules`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ courses, preferences }),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    
    if (!res.ok) {
      const error = await res.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `Request failed: ${res.status}`);
    }
    
    return res.json();
  } catch (err) {
    clearTimeout(timeout);
    console.error('API Error:', err);
    if (err.name === 'AbortError') {
      throw new Error('Request timed out. Try reducing course combinations or retrying.');
    }
    if (err.message === 'Failed to fetch') {
      throw new Error('Cannot reach backend. The server might be starting up or there may be a CORS issue.');
    }
    throw err;
  }
}
