// ViewerPage.js
import React from 'react';

function ViewerPage({ onLogout }) {
  return (
    <div style={{ padding: '2rem' }}>
      <h1>Welcome, Viewer</h1>
      <p>You have limited access. This is a read-only summary view.</p>
      <p>Future updates will include system uptime, public logs, etc.</p>
      <button onClick={onLogout} style={{ marginTop: '2rem' }}>Logout</button>
    </div>
  );
}

export default ViewerPage;

