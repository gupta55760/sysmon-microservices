import React, { useEffect, useState } from "react";
import AdminPanel from "./AdminPanel";
import { authFetch } from "./apiClient";
import {
  clearToken,
  getRoleFromToken,
  getToken,
  setToken,
} from "./authService";
import Login from "./Login";
import ViewerPage from "./ViewerPage";

function App() {
  const [role, setRole] = useState("");
  const [status, setStatus] = useState("");
  const [metrics, setMetrics] = useState(null);
  const [version, setVersion] = useState("");
  const [health, setHealth] = useState("");
  const [loggedOut, setLoggedOut] = useState(false);
  const [message, setMessage] = useState("");

  const handleUnauthorized = () => {
    setMessage("❌ Session expired. Please log in again.");
    setToken(null);
    setRole("");
    setLoggedOut(true);
  };

  const fetchStatus = async () => {
    try {
      //const res = await authFetch('http://localhost:8080/api/metrics/status');
      const res = await authFetch(
        "http://localhost:8080/api/metrics/status",
        {},
        handleUnauthorized
      );
      const data = await res.json();
      setStatus(data.status);
    } catch (err) {
      console.error("Status fetch error:", err.message);
    }
  };

  const fetchMetrics = async () => {
    try {
      const res = await authFetch(
        "http://localhost:8080/api/metrics/metrics",
        {},
        handleUnauthorized
      );
      const data = await res.json();
      setMetrics(data);
    } catch (err) {
      console.error("Metrics fetch error:", err.message);
    }
  };

  const fetchVersionAndHealth = async () => {
    try {
      const [verRes, healthRes] = await Promise.all([
        fetch("http://localhost:8080/api/metrics/version"),
        fetch("http://localhost:8080/api/metrics/health"),
      ]);
      const verData = await verRes.json();
      const healthData = await healthRes.json();
      setVersion(verData.version);
      setHealth(healthData.health);
    } catch (err) {
      console.error("Version/Health fetch error:", err.message);
    }
  };

  useEffect(() => {
    const token = getToken();
    if (token) {
      const role = getRoleFromToken(token);
      setRole(role);
    }

    if (!loggedOut && token) {
      fetchStatus();
      fetchMetrics();
      fetchVersionAndHealth();
    }

    // Auto logout on token expiry (poll every 10 seconds)
    const interval = setInterval(() => {
      const role = getRoleFromToken(getToken());
      if (!role) {
        console.warn("Token expired. Auto-logging out...");
        handleLogout();
      }
    }, 10000);

    return () => clearInterval(interval);
  }, [loggedOut]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleLogout = async () => {
    await fetch("http://localhost:8080/api/users/logout", {
      method: "POST",
      credentials: "include",
    });
    clearToken();
    setRole("");
    setLoggedOut(true);
    setMessage("");
  };

  if (!getToken()) {
    return (
      <Login
        onLogin={(tok) => {
          setToken(tok);
          setLoggedOut(false);
          setMessage("");
          const role = getRoleFromToken(tok);
          setRole(role);
        }}
      />
    );
  }

  if (role === "viewer") {
    return <ViewerPage onLogout={handleLogout} />;
  }

  return (
    <div style={{ padding: "2rem" }}>
      <h1>🖥️ SysMon Dashboard</h1>
      {message && (
        <p style={{ color: "red", marginTop: "1rem" }}>❌ {message}</p>
      )}
      <p>
        <strong>Status:</strong> {status || "Loading..."}
      </p>
      {role === "admin" && <AdminPanel metrics={metrics} />}
      <div style={{ textAlign: "right", marginTop: "1rem" }}>
        <button onClick={handleLogout}>Logout</button>
      </div>
      <footer
        style={{
          marginTop: "2rem",
          fontSize: "0.8rem",
          color: "gray",
          textAlign: "center",
          opacity: 0.7,
        }}
      >
        Metrics Service v{version} | Health: {health}
      </footer>
    </div>
  );
}

export default App;
