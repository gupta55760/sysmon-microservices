import React, { useState, useEffect } from 'react';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    console.log("Login - Always runs after first render");
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8080/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        credentials: 'include'  // ✅ receive HttpOnly cookie
      });

      if (!res.ok) {
        throw new Error('Login failed');
      }

      const data = await res.json();

      // ✅ Store access_token in memory only
      onLogin(data.access_token);
    } catch (err) {
      alert('Login error: ' + err.message);
    }
  };

  return (
    <form onSubmit={handleLogin} style={{ padding: '2rem' }}>
      <h2>Login to SysMon</h2>
      <div>
        <input
          type="text"
          placeholder="Username"
          value={username}
          required
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div style={{ marginTop: '1rem' }}>
        <input
          type="password"
          placeholder="Password"
          value={password}
          required
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <button type="submit" style={{ marginTop: '1rem' }}>Login</button>
    </form>
  );
}

export default Login;

