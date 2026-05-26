import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Shield, LayoutDashboard, History, BookOpen, LogOut, Key, User } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { currentUser, logout, isMockAuth } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/');
    } catch (error) {
      console.error("Failed to log out: ", error);
    }
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-cyber-dark border-b border-cyber-border sticky top-0 z-50 backdrop-blur-md bg-opacity-80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2 text-xl font-extrabold text-cyan-400 font-sans tracking-wide">
              <Shield className="h-6 w-6 text-cyan-400 stroke-[2] drop-shadow-[0_0_6px_rgba(0,240,255,0.5)]" />
              <span>Secure<span className="text-white">Repo</span></span>
            </Link>
            
            {currentUser && (
              <div className="hidden md:flex items-center space-x-1 ml-10">
                <Link 
                  to="/dashboard" 
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive('/dashboard') ? 'text-cyan-400 bg-cyan-950/30 border-b-2 border-cyan-400' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  <LayoutDashboard className="h-4 w-4" />
                  Dashboard
                </Link>
                <Link 
                  to="/history" 
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive('/history') ? 'text-cyan-400 bg-cyan-950/30 border-b-2 border-cyan-400' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  <History className="h-4 w-4" />
                  History
                </Link>
                <Link 
                  to="/learn" 
                  className={`flex items-center gap-1.5 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    isActive('/learn') ? 'text-cyan-400 bg-cyan-950/30 border-b-2 border-cyan-400' : 'text-slate-400 hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  <BookOpen className="h-4 w-4" />
                  Learn
                </Link>
              </div>
            )}
          </div>

          <div className="flex items-center gap-4">
            {isMockAuth && currentUser && (
              <span className="hidden lg:inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-950/30 text-amber-400 border border-amber-500/20">
                Demo Mode
              </span>
            )}
            
            {currentUser ? (
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="h-8 w-8 rounded-full bg-cyan-950 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-bold">
                    <User className="h-4 w-4" />
                  </div>
                  <span className="hidden sm:inline text-sm font-medium text-slate-300">
                    {currentUser.displayName || currentUser.email}
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium text-slate-400 hover:text-red-400 hover:bg-red-950/20 transition-all border border-transparent hover:border-red-500/20"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="hidden sm:inline">Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link 
                  to="/login"
                  className="text-sm font-medium text-slate-400 hover:text-white px-3 py-2 transition-colors"
                >
                  Log In
                </Link>
                <Link 
                  to="/register"
                  className="bg-cyan-600 hover:bg-cyan-500 text-white text-sm font-semibold px-4 py-2 rounded-lg transition-all shadow-lg hover:shadow-cyan-500/20"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Mobile nav indicator/bar */}
      {currentUser && (
        <div className="flex md:hidden border-t border-cyber-border justify-around py-2 bg-cyber-darkest/50">
          <Link 
            to="/dashboard" 
            className={`flex flex-col items-center p-1 text-xs ${isActive('/dashboard') ? 'text-cyan-400' : 'text-slate-500'}`}
          >
            <LayoutDashboard className="h-4 w-4 mb-0.5" />
            Dashboard
          </Link>
          <Link 
            to="/history" 
            className={`flex flex-col items-center p-1 text-xs ${isActive('/history') ? 'text-cyan-400' : 'text-slate-500'}`}
          >
            <History className="h-4 w-4 mb-0.5" />
            History
          </Link>
          <Link 
            to="/learn" 
            className={`flex flex-col items-center p-1 text-xs ${isActive('/learn') ? 'text-cyan-400' : 'text-slate-500'}`}
          >
            <BookOpen className="h-4 w-4 mb-0.5" />
            Learn
          </Link>
        </div>
      )}
    </nav>
  );
}
