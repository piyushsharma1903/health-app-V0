import React from "react";
import "./ReportModal.css"; // optional for styling

const ReportModal = ({ isOpen, onClose, imageUrl }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button onClick={onClose} className="close-btn">✖</button>
        <img src={imageUrl} alt="Report" style={{ maxWidth: "100%", maxHeight: "80vh" }} />
      </div>
    </div>
  );
};

export default ReportModal;
