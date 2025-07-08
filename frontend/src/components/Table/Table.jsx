import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Table.css";
import { FaFileAlt } from "react-icons/fa"; // import icon at top
import ReportModal from "../ReportModal/ReportModal";

const ReportTable = () => {
  const [reports, setReports] = useState([]);
  // State for modal
  // This will control the visibility of the modal and store the image URL
  const [modalOpen, setModalOpen] = useState(false);
  const [modalImage, setModalImage] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8000/api/reports/")
      .then(res => {
        setReports(res.data);
      })
      .catch(err => {
        console.error("❌ Failed to fetch reports:", err);
      });
  }, []);

  const handleDelete = (id) => {
    if (window.confirm("Delete this report?")) {
      axios.delete(`http://localhost:8000/api/reports/${id}/`)
        .then(() => {
          setReports(reports.filter(report => report.id !== id));
        })
        .catch(err => {
          console.error("❌ Deletion failed:", err);
        });
    }
  };
  const handleOpenModal = (imageUrl) => {
    setModalImage(`http://localhost:8000${imageUrl}`);
    setModalOpen(true);
  };

  return (
    <div className="report-table-container">
      <h2>Reports History</h2>
      <table className="report-table">
        <thead>
          <tr>
            <th>Report Date</th>
            <th>Report Type</th>
            <th>AI Summary</th>
            <th>Report Image</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {reports.length > 0 ? (
            reports.map((report) => (
              <tr key={report.id}>
                <td>{report.report_date || "N/A"}</td>
                <td>{report.report_type}</td>
                <td>
                  <button
                    className="view-btn"
                    onClick={() => alert(report.ai_summary || "No summary available.")}
                  >
                    View
                  </button>
                </td>
                <td>
                  <button
                     onClick={() =>{
                        setModalImage(`http://localhost:8000${report.original_file}`);
                        setModalOpen(true);
                      }}
                      style={{
                        backgroundColor: "none",
                        color: "#007bff",
                        padding: "6px 12px",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                      }}
                      title ="View Report Image"
                    >
                      <FaFileAlt/>
                    </button>
                </td>
                <td>
                  <button
                    className="delete-btn"
                    onClick={() => handleDelete(report.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4" style={{ textAlign: "center" }}>No reports yet</td>
            </tr>
          )}
        </tbody>
      </table>
      <ReportModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        imageUrl={modalImage}
      />
    </div>
  );
};

export default ReportTable;
