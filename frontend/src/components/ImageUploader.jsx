import React, { useState } from "react";
import axios from "axios";

const ImageUploader = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFile(e.target.files[0]);
    setResult("");
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      const res = await axios.post("http://localhost:8000/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data.prediction);
    } catch (err) {
      console.error(err);
      setResult("Error uploading image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto text-center mt-20 space-y-4">
      <h1 className="text-2xl font-semibold">🩺 Breast Cancer Detector</h1>
      <input
        type="file"
        onChange={handleChange}
        accept="image/png, image/jpeg"
        className="block w-full text-sm text-gray-500
                   file:mr-4 file:py-2 file:px-4
                   file:rounded-full file:border-0
                   file:text-sm file:font-semibold
                   file:bg-pink-50 file:text-pink-700
                   hover:file:bg-pink-100"
      />
      <button
        onClick={handleUpload}
        disabled={!file}
        className="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded-lg"
      >
        {loading ? "Analyzing..." : "Upload & Predict"}
      </button>

      {result && (
        <div className="mt-4 text-lg font-medium">
          Prediction:{" "}
          <span
            className={
              result === "malignant" ? "text-red-600" : "text-green-600"
            }
          >
            {result.toUpperCase()}
          </span>
        </div>
      )}
    </div>
  );
};

export default ImageUploader;
