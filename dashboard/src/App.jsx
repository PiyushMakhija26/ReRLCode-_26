import React, { useState, useEffect, useRef } from 'react';
import './Dashboard.css';

function App() {
  const [data, setData] = useState(null);
  const [connected, setConnected] = useState(false);
  const canvasRef = useRef(null);
  const ws = useRef(null);

  useEffect(() => {
    // Initialize WebSocket
    const connect = () => {
      const hostname = window.location.hostname || '127.0.0.1';
      ws.current = new WebSocket(`ws://${hostname}:7777/ws/simulation`);
      
      ws.current.onopen = () => {
        console.log('Connected to Simulation Engine');
        setConnected(true);
      };
      
      ws.current.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          setData(payload);
        } catch (e) {
          console.error('Error parsing simulation data');
        }
      };
      
      ws.current.onclose = () => {
        console.log('Disconnected. Retrying in 3s...');
        setConnected(false);
        setTimeout(connect, 3000);
      };
    };

    connect();
    return () => ws.current?.close();
  }, []);

  useEffect(() => {
    if (!data || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const gridSize = data.grid_size;
    const cellSize = canvas.width / gridSize;

    // 1. Clear Canvas
    ctx.fillStyle = '#05060b';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Draw Grid Lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= gridSize; i++) {
      ctx.beginPath();
      ctx.moveTo(i * cellSize, 0);
      ctx.lineTo(i * cellSize, canvas.height);
      ctx.stroke();
      
      ctx.beginPath();
      ctx.moveTo(0, i * cellSize);
      ctx.lineTo(canvas.width, i * cellSize);
      ctx.stroke();
    }

    // 3. Draw Targets (Package Spots)
    data.targets.forEach(t => {
      const isReached = data.agents.some(a => a.id === t.id && a.reached);
      
      ctx.shadowBlur = isReached ? 20 : 0;
      ctx.shadowColor = '#00ff88';
      ctx.strokeStyle = isReached ? '#00ff88' : '#00d4ff';
      ctx.lineWidth = 3;
      
      // Draw a "package" square
      ctx.strokeRect(t.y * cellSize + 10, t.x * cellSize + 10, cellSize - 20, cellSize - 20);
      
      if (!isReached) {
        ctx.fillStyle = 'rgba(0, 212, 255, 0.1)';
        ctx.fillRect(t.y * cellSize + 12, t.x * cellSize + 12, cellSize - 24, cellSize - 24);
      }
    });

    // 4. Draw Agents (Robots)
    data.agents.forEach(a => {
      const color = a.reached ? '#00ff88' : '#ff3e3e';
      const shadowColor = a.reached ? 'rgba(0, 255, 136, 0.5)' : 'rgba(255, 62, 62, 0.5)';
      
      ctx.shadowBlur = 15;
      ctx.shadowColor = shadowColor;
      ctx.fillStyle = color;
      
      ctx.beginPath();
      ctx.arc(a.y * cellSize + cellSize / 2, a.x * cellSize + cellSize / 2, cellSize / 3, 0, Math.PI * 2);
      ctx.fill();
      
      // Label ID
      ctx.shadowBlur = 0;
      ctx.fillStyle = '#fff';
      ctx.font = '10px RobotoMono';
      ctx.textAlign = 'center';
      ctx.fillText(`R-${a.id}`, a.y * cellSize + cellSize / 2, a.x * cellSize + cellSize / 2 + 30);
    });

  }, [data]);

  return (
    <div className="dashboard-container">
      <header className="header">
        <div style={{display: 'flex', alignItems: 'center'}}>
           <div className="live-indicator"></div>
           <h1>Neo-Grid Logistics Control</h1>
        </div>
        <div className="status-badge">
          {connected ? 'LIVE ENGINE CONNECTED' : 'AWAITING BRAIN...'}
        </div>
      </header>
      
      <aside className="sidebar sidebar-l">
        <div className="stats-card">
          <h3>Simulation Step</h3>
          <div className="stats-value">{data?.step || 0}</div>
        </div>
        <div className="stats-card">
          <h3>Total Reward</h3>
          <div className="stats-value" style={{color: '#00ff88'}}>
            {data?.reward?.toFixed(2) || '0.00'}
          </div>
        </div>
        <div className="stats-card">
          <h3>Active Agents</h3>
          <div className="stats-value">
            {data?.agents?.filter(a => !a.reached).length || 0} / {data?.agents?.length || 0}
          </div>
        </div>
      </aside>
      
      <main className="main-view">
        <canvas 
          ref={canvasRef} 
          width={600} 
          height={600}
        ></canvas>
        {!connected && (
          <div style={{position: 'absolute', background: 'rgba(0,0,0,0.8)', padding: '20px', borderRadius: '10px'}}>
             Connecting to RL Engine...
          </div>
        )}
      </main>
      
      <aside className="sidebar sidebar-r">
        <h3>Agent Telemetry</h3>
        <div className="agent-list" style={{marginTop: '20px'}}>
           {data?.agents?.map(a => (
             <div key={a.id} className="agent-item">
               <span className="agent-id">ROBOT {a.id}</span>
               <span className="agent-status" style={{color: a.reached ? '#00ff88' : '#7a8aa7'}}>
                 {a.reached ? 'DELIVERED' : `AT [${a.x}, ${a.y}]`}
               </span>
             </div>
           ))}
        </div>
      </aside>
    </div>
  );
}

export default App;
