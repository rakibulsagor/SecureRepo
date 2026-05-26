import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Report from './pages/Report';
import History from './pages/History';
import Learn from './pages/Learn';

// Protected Route Wrapper
function ProtectedRoute({ children }) {
  const { currentUser, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-cyber-darkest">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-cyan-400"></div>
      </div>
    );
  }
  
  if (!currentUser) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

export default function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-cyber-darkest flex flex-col font-sans select-none">
          <Navbar />
          
          <main className="flex-1 pb-16">
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/report/:scanId" element={<Report />} />

              {/* Protected Routes */}
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/history" 
                element={
                  <ProtectedRoute>
                    <History />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/learn" 
                element={
                  <ProtectedRoute>
                    <Learn />
                  </ProtectedRoute>
                } 
              />

              {/* Fallback Catch-all redirect to Home */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
          
          {/* Global Cyberpunk themed footer */}
          <footer className="bg-cyber-dark border-t border-cyber-border/40 py-6 text-center text-xs text-slate-500">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-1">
              <p>© {new Date().getFullYear()} SecureRepo. Designed for CS Students Pair-Programming and Security Auditing.</p>
              <p className="text-[10px] text-slate-600 font-mono">Status: Secure • Rule-Based Regex Engines Active • Gemini AI Helper Ready</p>
            </div>
          </footer>
        </div>
      </AuthProvider>
    </Router>
  );
}
