import React from "react";

const SectionCard = ({ title, children }) => {
  return (
    <div style={{
      border: "1px solid #ddd",
      borderRadius: "8px",
      padding: "1.5rem",
      marginBottom: "2rem",
      backgroundColor: "#f9f9f9",
      boxShadow: "0 1px 4px rgba(0,0,0,0.06)"
    }}>
      {title && (
        <h2 style={{
          marginTop: 0,
          fontSize: "1.2rem",
          fontWeight: "bold",
          borderBottom: "1px solid #ccc",
          paddingBottom: "0.5rem",
          marginBottom: "1rem"
        }}>{title}</h2>
      )}
      {children}
    </div>
  );
};

export default SectionCard;

