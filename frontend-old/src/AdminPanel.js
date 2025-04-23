import React, { useState, useEffect } from 'react';
import { authFetch, getToken } from './authService';

function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState({ username: '', password: '', role: 'user' });
  const [message, setMessage] = useState('');

  const accessToken = getToken();

  const fetchUsers = async () => {
    try {
      const res = await authFetch('http://localhost:8080/api/users');
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
    fetchUsers();
  }, []);

  const handleCreate = async () => {
    if (!form.username || !form.password) {
      setMessage('❌ Username and password are required');
      return;
    }

    if (users.find((u) => u.username === form.username)) {
      setMessage('❌ User already exists');
      return;
    }

    try {
      const res = await authFetch('http://localhost:8080/api/users/create_user', accessToken, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });

      if (res.ok) {
        setMessage('✅ User created');
        setForm({ username: '', password: '', role: 'user' });
        fetchUsers();
      } else {
        const err = await res.json();
        setMessage(`❌ Error: ${err.detail || 'Could not create user'}`);
      }
    } catch (err) {
      setMessage(`❌ Request failed: ${err.message}`);
    }
  };

  const handleDelete = async (username) => {
    const confirm = window.confirm(`Are you sure you want to delete user "${username}"?`);
    if (!confirm) return;

    try {
      const res = await authFetch(`http://localhost:8080/api/users/${username}`, accessToken, {
        method: 'DELETE',
      });

      if (res.ok) {
        setMessage('✅ User deleted');
        await fetchUsers();
        setTimeout(() => setMessage(''), 3000);
      } else {
        setMessage('❌ Failed to delete user');
      }
    } catch (err) {
      setMessage(`❌ Delete failed: ${err.message}`);
    }
  };

  return (
    <div>
      <h2>👩‍💼 Admin Panel</h2>

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

      <h3>Existing Users</h3>
      <ul>
        {users.map((user) => (
          <li key={user.username}>
            {user.username} ({user.role}){' '}
            <button onClick={() => handleDelete(user.username)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default AdminPanel;

