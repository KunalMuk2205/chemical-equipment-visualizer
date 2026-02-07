import React, { useState } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/upload/', formData, {
        auth: { username: 'Kunal2205', password: 'Kunal' }
      });
      
      setData(response.data);
      setHistory(prev => [{ 
        name: file.name, 
        temp: response.data.avg_temp, 
        status: response.data.status, 
        time: new Date().toLocaleTimeString() 
      }, ...prev]);
    } catch (error) {
      alert("Backend error. Ensure Django is running and credentials are correct.");
    } finally {
      setLoading(false);
    }
  };

  const downloadPDF = () => {
    window.open(`http://127.0.0.1:8000/api/upload/?export=pdf`, '_blank');
  };

  return (
    <div className="min-h-screen bg-[#0f172a] text-slate-200 font-sans flex flex-col">
      {/* Navigation */}
      <nav className="border-b border-slate-800 bg-[#0f172a]/80 backdrop-blur-md sticky top-0 z-10 p-4 px-8 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <div className="bg-blue-600 w-8 h-8 rounded flex items-center justify-center font-bold text-white italic">C</div>
          <h1 className="text-xl font-bold tracking-tight text-white">CHEM-ANALYTICS <span className="text-blue-500 text-sm">PRO</span></h1>
        </div>
        <div className="flex items-center gap-4">
          {data && (
            <button 
              onClick={downloadPDF}
              className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-1.5 rounded-lg text-xs font-bold transition flex items-center gap-2"
            >
              📄 EXPORT PDF
            </button>
          )}
          <div className="text-xs font-mono text-slate-500">STATUS: <span className="text-emerald-500">CONNECTED</span></div>
        </div>
      </nav>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-72 border-r border-slate-800 p-6 flex flex-col gap-6 overflow-y-auto">
          <div>
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Actions</h3>
            <label className={`flex flex-col items-center justify-center w-full p-4 border-2 border-dashed rounded-xl cursor-pointer transition-all ${loading ? 'border-slate-800 bg-slate-900 cursor-not-allowed' : 'border-slate-700 hover:border-blue-500 hover:bg-slate-800'}`}>
              <span className="text-sm font-medium text-blue-400">
                {loading ? '⌛ Processing...' : '+ Upload CSV'}
              </span>
              <input type="file" className="hidden" onChange={handleUpload} accept=".csv" disabled={loading} />
            </label>
            
            {/* NEW: Download Sample Template Link */}
            <div className="mt-4 p-3 bg-blue-500/5 border border-blue-500/20 rounded-lg">
                <p className="text-[10px] text-slate-500 uppercase font-bold mb-1">Testing Tool</p>
                <a 
                    href="http://127.0.0.1:8000/api/sample/" 
                    className="text-xs text-blue-400 hover:text-blue-300 flex items-center gap-1 font-medium"
                >
                    ⬇ Download Sample CSV
                </a>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Recent Sessions</h3>
            <div className="space-y-3">
              {history.length > 0 ? history.map((item, i) => (
                <div key={i} className={`p-3 border rounded-lg text-xs ${item.status === 'Warning' ? 'bg-red-900/20 border-red-900/50' : 'bg-slate-800/50 border-slate-700'}`}>
                  <p className="text-white font-medium truncate">{item.name}</p>
                  <div className="flex justify-between mt-2 text-slate-500">
                    <span className={item.status === 'Warning' ? 'text-red-400 font-bold' : ''}>{item.temp}°C</span>
                    <span>{item.time}</span>
                  </div>
                </div>
              )) : (
                <p className="text-xs text-slate-600 italic">No history yet</p>
              )}
            </div>
          </div>
        </aside>

        {/* Main Dashboard */}
        <main className="flex-1 p-8 overflow-y-auto bg-slate-950/50">
          {loading && <div className="fixed top-0 left-0 w-full h-1 bg-blue-500 animate-pulse z-50"></div>}

          {data ? (
            <div className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <StatCard label="Total Units" val={data.total_count} color="text-blue-500" />
                <StatCard label="Avg Temp" val={`${data.avg_temp}°C`} color="text-orange-500" />
                <StatCard label="Avg Pressure" val={`${data.avg_pressure} bar`} color="text-emerald-500" />
                
                <div className={`p-6 rounded-2xl border shadow-xl transition-all ${data.outlier_alerts > 0 ? 'bg-red-950/30 border-red-500/50 animate-pulse' : 'bg-[#1e293b] border-slate-800'}`}>
                  <p className="text-slate-500 text-xs font-bold uppercase tracking-tighter">System Health</p>
                  <p className={`text-xl font-black mt-1 ${data.outlier_alerts > 0 ? 'text-red-500' : 'text-emerald-500'}`}>
                    {data.status} {data.outlier_alerts > 0 && `(${data.outlier_alerts} Outliers)`}
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ChartWrapper title="Unit Frequency">
                  <Bar 
                    data={{
                      labels: Object.keys(data.type_distribution),
                      datasets: [{ label: 'Count', data: Object.values(data.type_distribution), backgroundColor: '#3b82f6', borderRadius: 4 }]
                    }}
                    options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } } }}
                  />
                </ChartWrapper>

                <ChartWrapper title="Composition (%)">
                  <Pie 
                    data={{
                      labels: Object.keys(data.type_distribution),
                      datasets: [{
                        data: Object.values(data.type_distribution),
                        backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
                        borderWidth: 0
                      }]
                    }}
                    options={{ responsive: true, maintainAspectRatio: false }}
                  />
                </ChartWrapper>
              </div>
            </div>
          ) : (
            <div className="h-full flex flex-col items-center justify-center text-slate-600">
              <div className="mb-4 opacity-20">
                <svg width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
              </div>
              <p className="text-xl font-medium italic">Dashboard Idle - Waiting for CSV input</p>
              <p className="text-sm mt-2 text-slate-700 uppercase tracking-widest font-bold">Please upload a valid chemical dataset</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

const StatCard = ({ label, val, color }) => (
  <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800 shadow-xl">
    <p className="text-slate-500 text-xs font-bold uppercase tracking-tighter">{label}</p>
    <p className={`text-3xl font-black mt-1 ${color}`}>{val}</p>
  </div>
);

const ChartWrapper = ({ title, children }) => (
  <div className="bg-[#1e293b] p-6 rounded-2xl border border-slate-800 shadow-xl">
    <h3 className="text-sm font-bold text-slate-400 mb-6 uppercase tracking-wider">{title}</h3>
    <div className="h-64">{children}</div>
  </div>
);

export default App;