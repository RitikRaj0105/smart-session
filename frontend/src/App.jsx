import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState("Disconnected 🔴");
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    // 1. Connect to the Teacher WebSocket Endpoint
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/teacher");

    // 2. When connection opens
    socket.onopen = () => {
      setStatus("Connected 🟢");
      console.log("Websocket Connected!");
    };

    // 3. When backend sends an alert (Proctor Alert)
    socket.onmessage = (event) => {
      console.log("New Message:", event.data);
      try {
        const data = JSON.parse(event.data);
        // Add new alert to the top of the list
        setAlerts((prev) => [data, ...prev]);
      } catch (error) {
        console.error("Error parsing JSON:", error);
      }
    };

    // 4. When connection closes
    socket.onclose = () => {
      setStatus("Disconnected 🔴");
    };

    // Cleanup when leaving the page
    return () => socket.close();
  }, []);

  return (
    <div className="App">
      <h1>👨‍🏫 Smart Session Dashboard</h1>
      
      {/* Connection Status Badge */}
      <div style={{ padding: '10px', background: '#f0f0f0', borderRadius: '8px', marginBottom: '20px' }}>
        <strong>System Status:</strong> {status}
      </div>

      {/* Alerts Feed */}
      <div className="card">
        <h3>Live Proctor Feed</h3>
        {alerts.length === 0 ? (
          <p style={{ color: '#888' }}>Waiting for student activity...</p>
        ) : (
          <div style={{ textAlign: 'left' }}>
            {alerts.map((alert, index) => (
              <div key={index} style={{ 
                padding: '10px', 
                borderBottom: '1px solid #eee',
                backgroundColor: alert.status === "PROCTOR_ALERT" ? '#ffebee' : '#e8f5e9',
                color: alert.status === "PROCTOR_ALERT" ? '#c62828' : '#2e7d32'
              }}>
                <strong>{alert.student_id}:</strong> {alert.status} 
                <span style={{ fontSize: '0.8em', color: '#555', marginLeft: '10px' }}>
                   (Emotion: {alert.raw_emotion || 'N/A'})
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default App