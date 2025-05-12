import React, { useEffect, useState } from "react";
import { authFetch } from "./apiClient";
import { getToken } from "./authService";
import FeedbackPanel from "./FeedbackPanel";
import SectionCard from "./SectionCard";

function AdminPanel({ metrics }) {
  console.log("📊 METRICS:", metrics);
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({
    username: "",
    password: "",
    role: "user",
  });
  const [message, setMessage] = useState("");

  const accessToken = getToken();

  const fetchUsers = async () => {
    try {
      const res = await authFetch("http://localhost:8080/api/users");
      if (!res.ok) {
        const errorText = await res.text(); // handle non-JSON errors
        throw new Error(`HTTP ${res.status} - ${errorText}`);
      }

      const data = await res.json();
      if (Array.isArray(data.users)) {
        setUsers(data.users);
      } else {
        console.log("No users returned in fetchUsers...");
        setUsers([]);
      }
    } catch (err) {
      setMessage(`❌ Fetch users failed: ${err.message}`);
    }
  };

  useEffect(() => {
    console.log("In useEffect of AdminPanel...");
    fetchUsers();
  }, []);

  const handleCreate = async () => {
    if (!form.username || !form.password) {
      setMessage("❌ Username and password are required");
      return;
    }

    if (users.find((u) => u.username === form.username)) {
      setMessage("❌ User already exists");
      return;
    }

    try {
      const res = await authFetch(
        "http://localhost:8080/api/users/create_user",
        accessToken,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(form),
        }
      );

      if (res.ok) {
        setMessage("✅ User created");
        setForm({ username: "", password: "", role: "user" });
        fetchUsers();
      } else {
        const err = await res.json();
        setMessage(`❌ Error: ${err.detail || "Could not create user"}`);
      }
    } catch (err) {
      setMessage(`❌ Request failed: ${err.message}`);
    }
  };

  const handleDelete = async (username) => {
    const confirm = window.confirm(
      `Are you sure you want to delete user "${username}"?`
    );
    if (!confirm) return;

    try {
      const res = await authFetch(
        `http://localhost:8080/api/users/${username}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            "Content-Type": "application/json",
          },
        }
      );

      if (res.ok) {
        setMessage("✅ User deleted");
        await fetchUsers();
        setTimeout(() => setMessage(""), 3000);
      } else {
        setMessage("❌ Failed to delete user");
      }
    } catch (err) {
      setMessage(`❌ Delete failed: ${err.message}`);
    }
  };

  return (
    <main style={{ maxWidth: "800px", margin: "auto", padding: "2rem" }}>
      <div style={{ marginTop: "2rem" }}>
        <SectionCard title="📊 Metrics">
          {!metrics ? (
            <p>Loading system metrics...</p>
          ) : (
            <ul>
              <li>
                <strong>Hostname:</strong> {metrics.hostname || "N/A"}
              </li>
              <li>
                <strong>Platform:</strong> {metrics.platform || "N/A"}
              </li>
              <li>
                <strong>Platform Version:</strong>{" "}
                {metrics.platform_version || "N/A"}
              </li>
              <li>
                <strong>Uptime:</strong>{" "}
                {metrics.uptime_secs != null
                  ? `${(metrics.uptime_secs / 3600).toFixed(1)} hrs`
                  : "N/A"}
              </li>
              <li>
                <strong>CPU Count:</strong> {metrics.cpu?.cores ?? "N/A"}
              </li>
              <li>
                <strong>CPU Load %:</strong> {metrics.cpu?.percent ?? "N/A"}%
              </li>
              <li>
                <strong>Memory Used %:</strong>{" "}
                {metrics.memory?.percent ?? "N/A"}%
              </li>
              <li>
                <strong>Disk Used %:</strong> {metrics.disk?.percent ?? "N/A"}%
              </li>
              <li>
                <strong>Timestamp:</strong>{" "}
                {new Date(metrics.timestamp).toLocaleString()}
              </li>
            </ul>
          )}
        </SectionCard>
      </div>

      <div style={{ marginTop: "2rem" }}>
        <SectionCard title="👩‍💼 Admin Panel">
          {message && <p>{message}</p>}

          <h3>Create User</h3>
          <input
            type="text"
            placeholder="Username"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
          />
          <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <select
            value={form.role}
            onChange={(e) => setForm({ ...form, role: e.target.value })}
          >
            <option value="user">user</option>
            <option value="admin">admin</option>
            <option value="viewer">viewer</option>
          </select>
          <button onClick={handleCreate}>Create</button>

          <h3 style={{ marginTop: "1.5rem" }}>Existing Users</h3>
          <ul>
            {users.map((user) => (
              <li key={user.username}>
                {user.username} ({user.role}){" "}
                <button
                  onClick={() => handleDelete(user.username)}
                  style={{
                    fontSize: "0.8rem",
                    backgroundColor: "#eee",
                    border: "1px solid #ccc",
                    padding: "2px 6px",
                    marginLeft: "0.5rem",
                  }}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        </SectionCard>
      </div>

      <div style={{ marginTop: "2rem" }}>
        <SectionCard title="📝 Recent Feedback">
          <FeedbackPanel />
        </SectionCard>
      </div>
    </main>
  );
}

export default AdminPanel;
