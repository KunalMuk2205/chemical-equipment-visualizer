import React, { useState } from 'react';
import axios from 'axios';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Registering Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      // Connects to your Django server at port 8000
      const response = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
      auth: {
              username: 'Kunal2205',
              password: 'Kunal'
      }
});
      setData(response.data);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Backend is not responding. Is Django running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '40px', textAlign: 'center', fontFamily: 'sans-serif' }}>
      <h1>Chemical Equipment Visualizer</h1>
      <div style={{ margin: '20px' }}>
        <input type="file" onChange={handleUpload} accept=".csv" />
      </div>

      {loading && <p>Processing CSV...</p>}

      {data && (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-around', background: '#f4f4f4', padding: '10px', borderRadius: '8px' }}>
            <p><strong>Total Items:</strong> {data.total_count}</p>
            <p><strong>Avg Temp:</strong> {data.avg_temp}°C</p>
            <p><strong>Avg Pressure:</strong> {data.avg_pressure} bar</p>
          </div>

          <div style={{ marginTop: '40px' }}>
            <h3>Equipment Type Distribution</h3>
            <Bar 
              data={{
                labels: Object.keys(data.type_distribution),
                datasets: [{
                  label: 'Count',
                  data: Object.values(data.type_distribution),
                  backgroundColor: 'rgba(54, 162, 235, 0.6)',
                }]
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;