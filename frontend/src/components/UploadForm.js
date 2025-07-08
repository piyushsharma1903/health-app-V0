import React, { useState } from "react";
import axios from "axios";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [reportType, setReportType] = useState("lab");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !reportType) return;

    const formData = new FormData();
    formData.append("original_file", file);
    formData.append("report_type", reportType);

    setLoading(true);
    setResult(null);

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/upload-lab/", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setResult({ error: "Something went wrong. Check the console." });
    }

    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow-xl rounded-lg">
      <h1 className="text-2xl font-bold mb-4 text-center">Upload Medical Report</h1>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="file"
          accept=".png,.jpg,.jpeg,.pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="border p-2 rounded"
        />

        <select
          value={reportType}
          onChange={(e) => setReportType(e.target.value)}
          className="border p-2 rounded"
        >
          <option value="lab">Lab Report</option>
          <option value="ct">CT Scan</option>
          <option value="mri">MRI</option>
        </select>

        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded"
        >
          {loading ? "Uploading..." : "Submit"}
        </button>
      </form>

      {result && (
        <div className="mt-6 p-4 border rounded bg-gray-50 text-sm whitespace-pre-wrap">
          <strong>Server Response:</strong>
          <br />
          {JSON.stringify(result, null, 2)}
        </div>
      )}
    </div>
  );
}
