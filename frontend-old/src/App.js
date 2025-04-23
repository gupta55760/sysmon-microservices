import React, { useState, useEffect } from 'react';
import Login from './Login';
import AdminPanel from './AdminPanel';
import ViewerPage from './ViewerPage';
import { jwtDecode } from 'jwt-decode';
import {
  authFetch,
  getToken,
  setToken,
  refreshAccessToken,
} from './authService';

function App() {
  const [role, setRole] = useState('');
  const [status, setStatus] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [version, setVersion] = useState('');
  const [health, setHealth] = useState('');
  const [loggedOut, setLoggedOut] = useState(false); // ✅ track logout

  useEffect(() => {
    const token = getToken();
    if (token) {
      try {
        const decoded = jwtDecode(token);
        setRole(decoded.role || '');
      } catch (err) {
        console.error('Failed to decode token', err);
        setRole('');
      }
    }
  }, []);

  useEffect(() => {
    const tryRefresh = async () => {
      try {
        const token = await refreshAccessToken();
        const decoded = jwtDecode(token);
        setToken(token);
        setRole(decoded.role || '');
      } catch (err) {
        console.warn('No valid refresh token available.');
      }
    };

    // ✅ Avoid refresh if we just logged out
    if (!getToken() && role === '' && !loggedOut) {
      tryRefresh();
    }
  }, [role, loggedOut]);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const versionRes = await fetch('http://localhost:8080/api/metrics/version');
        const versionData = await versionRes.json();
        setVersion(versionData.version || '');
      } catch (err) {
        setVersion('unknown');
      }

      try {
        const healthRes = await fetch('http://localhost:8080/api/metrics/health');
        setHealth(healthRes.ok ? 'healthy' : 'unreachable');
      } catch (err) {
        setHealth('error');
      }
    };

    fetchStatus();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const statusRes = await authFetch('http://localhost:8080/api/metrics/status');
        const metricsRes = await authFetch('http://localhost:8080/api/metrics/metrics');
        const statusData = await statusRes.json();
        const metricsData = await metricsRes.json();
        setStatus(statusData.status);
        setMetrics(metricsData);
      } catch (err) {
        console.error('Failed to fetch system data', err);
      }
    };

    if (getToken()) {
      fetchData();
    }
  }, [role]);

  const handleLogout = async () => {
    try {
      const res = await fetch('http://localhost:8080/api/users/logout', {
        method: 'POST',
        credentials: 'include',
      });
  
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Logout failed: ${res.status} - ${errorText}`);
      }
  
      setToken(null);
      setRole('');
      setLoggedOut(true); // ✅ prevent refresh call
    } catch (err) {
      console.error('Logout error:', err);
      alert(`Logout failed: ${err.message}`);
    }
  };


  if (!getToken()) {
    return (
      <Login
        onLogin={(tok) => {
          setToken(tok);
          setLoggedOut(false); // ✅ reset logout flag
          const decoded = jwtDecode(tok);
          setRole(decoded.role || '');
        }}
      />
    );
  }

  if (role === 'viewer') {
    return <ViewerPage onLogout={handleLogout} />;
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>SysMon Dashboard</h1>
      <p><strong>Status:</strong> {status || 'Loading...'}</p>
      {metrics ? (
        <div>
          <p><strong>Metrics:</strong></p>
          <ul>
            {Object.entries(metrics).map(([key, value]) => (
              <li key={key}>
                {key}: {typeof value === 'object' ? JSON.stringify(value) : value}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p><strong>Metrics:</strong> Loading...</p>
      )}
      {role === 'admin' && <AdminPanel />}
      <button onClick={handleLogout} style={{ marginTop: '2rem' }}>Logout</button>
      <footer style={{ marginTop: '2rem', fontSize: '0.8rem', color: 'gray' }}>
        Metrics Service v{version} | Health: {health}
      </footer>
    </div>
  );
}

export default App;

