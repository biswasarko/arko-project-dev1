import React, { useState, useEffect } from 'react';

function Dashboard() {
  const [rows, setRows] = useState([]);

  useEffect(() => {
    const fetchMonthEndRows = async () => {
      const response = await fetch('http://localhost:5000/month-end');
      const data = await response.json();
      if (response.ok) {
        setRows(data.rows);
      } else {
        alert(`Error: ${data.error}`);
      }
    };

    fetchMonthEndRows();
  }, []);

  return (
    <div>
      <h2>Month-End Rows</h2>
      <table border="1">
        <thead>
          <tr>
            {rows.length > 0 &&
              Object.keys(rows[0]).map((header) => <th key={header}>{header}</th>)}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={index}>
              {Object.values(row).map((value, i) => (
                <td key={i}>{value}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Dashboard;
