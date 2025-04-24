import React, { useEffect, useState } from "react";
import { authFetch } from "./apiClient";

const FeedbackPanel = () => {
  const [feedback, setFeedback] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchFeedback = async () => {
      try {
        const res = await authFetch("http://localhost:8080/api/feedback");
        if (!res.ok) {
          const msg = await res.text();
          throw new Error(`HTTP ${res.status}: ${msg}`);
        }
        const data = await res.json();
        setFeedback(data);
      } catch (err) {
        setError(`❌ Failed to load feedback: ${err.message}`);
      }
    };

    fetchFeedback();
  }, []);

  return (
    <div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {feedback.length === 0 ? (
        <p>No feedback found.</p>
      ) : (
        <ul>
          {feedback.map((f, idx) => (
            <li key={idx}>
              <strong>{f.firstname} {f.lastname}</strong>: {f.comments} ({f.rating}⭐)  
              <br />
              <small>{new Date(f.timestamp).toLocaleString('en-US', {
                dateStyle: 'medium',
                timeStyle: 'short'
              })}</small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default FeedbackPanel;

