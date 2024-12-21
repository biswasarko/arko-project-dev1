import React, { useState } from 'react';

function UploadForm() {
  const [columns, setColumns] = useState([]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    if (response.ok) {
      setColumns(data.columns);
      alert('File uploaded successfully!');
    } else {
      alert(`Error: ${data.error}`);
    }
  };

  return (
    <div>
      <h2>Upload Excel File</h2>
      <input type="file" accept=".xlsx" onChange={handleFileUpload} />
    </div>
  );
}

export default UploadForm;
