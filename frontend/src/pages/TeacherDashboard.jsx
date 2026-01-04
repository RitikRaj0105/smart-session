import React, { useEffect, useState } from 'react';
// Assume using Recharts for timeline
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const TeacherDashboard = () => {
  const [status, setStatus] = useState("WAITING");
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/teacher');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setStatus(data.status);
      
      // Update chart history
      setHistory(prev => {
        const newState = [...prev, { 
            time: new Date().toLocaleTimeString(), 
            value: data.status === "FOCUSED" ? 1 : (data.status === "CONFUSED" ? 0.5 : 0) 
        }];
        return newState.slice(-20); // Keep last 20 points
      });
    };

    return () => ws.close();
  }, []);

  // Dynamic Color Logic
  const getStatusColor = () => {
    if (status === "PROCTOR_ALERT") return "bg-red-600";
    if (status === "CONFUSED") return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Teacher "Super Vision" Dashboard</h1>
      
      <div className={`p-10 rounded-xl text-white text-center text-4xl font-bold ${getStatusColor()}`}>
        {status.replace("_", " ")}
      </div>

      <div className="mt-8 h-64 w-full border rounded-lg p-4">
        <h3 className="mb-4 text-gray-700">Engagement Timeline</h3>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={history}>
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="value" stroke="#8884d8" strokeWidth={2} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default TeacherDashboard;