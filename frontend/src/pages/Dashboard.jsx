import React from 'react';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { logout } = useAuth();

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Affiliate Dashboard</h2>
      <p>Welcome! You are securely logged in.</p>
      <button onClick={logout}>Log Out</button>
    </div>
  );
}