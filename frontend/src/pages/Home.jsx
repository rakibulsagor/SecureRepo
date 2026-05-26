import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, ShieldAlert, Zap, BookOpen, Star, RefreshCw, Terminal, Cpu } from 'lucide-react';
import RepoInput from '../components/RepoInput';
import LoadingScan from '../components/LoadingScan';
import { scanApi } from '../api/scanApi';
import { useAuth } from '../context/AuthContext';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const { currentUser } = useAuth();
  const navigate = useNavigate();

  const handleScan = async (repoUrl, useAi) => {
    setIsLoading(true);
    setError('');

    try {
      // Pass the current user ID if logged in, otherwise default anonymous
      const userId = currentUser ? currentUser.uid : 'anonymous';
      const scanResult = await scanApi.runScan(repoUrl, userId, useAi);
      
      // Let the loading screen stay for a tiny bit so the logs feel natural
      setTimeout(() => {
        navigate(`/report/${scanResult.scan_id}`);
      }, 500);
    } catch (err) {
      console.error(err);
      const errMsg = err.response?.data?.detail || 'Scan failed. Make sure the repository is public and git is installed.';
      setError(errMsg);
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-16">
      {/* Hero Header */}
      <div className="text-center space-y-6 max-w-4xl mx-auto py-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-cyan-950/40 text-cyan-400 border border-cyan-500/20 shadow-glow-cyan/5">
          <Shield className="h-3.5 w-3.5" />
          <span>Next-Generation Security for Student Developers</span>
        </div>
        
        <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white leading-tight">
          Secure Your Code Before <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-sky-400 to-purple-500">
            Recruiters or Attackers See It
          </span>
        </h1>
        
        <p className="text-lg text-slate-400 max-w-2xl mx-auto font-sans leading-relaxed">
          SecureRepo scans your public GitHub repositories for leaked credentials, weak package dependencies, outdated runtime versions, and config flaws, explaining how to fix them in plain English.
        </p>
      </div>

      {/* Scanner Input / Loading Panel */}
      <div className="py-2">
        {isLoading ? (
          <LoadingScan />
        ) : (
          <div className="space-y-4">
            <RepoInput onScan={handleScan} isLoading={isLoading} />
            {error && (
              <div className="max-w-3xl mx-auto p-4 bg-red-950/20 border border-red-500/20 text-red-400 rounded-xl text-sm flex items-start gap-3">
                <ShieldAlert className="h-5 w-5 flex-shrink-0 mt-0.5" />
                <div>
                  <h5 className="font-bold text-white mb-0.5">Scanning Error</h5>
                  <p>{error}</p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Feature Pitch Grid */}
      <div className="grid md:grid-cols-3 gap-8 pt-10">
        <div className="cyber-card hover:-translate-y-1 duration-300">
          <div className="h-10 w-10 rounded-lg bg-cyan-950 border border-cyan-500/20 flex items-center justify-center text-cyan-400 mb-4 shadow-md shadow-cyan-500/10">
            <Cpu className="h-5 w-5" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Deterministic Scanning</h3>
          <p className="text-sm text-slate-400 leading-relaxed font-sans">
            We use rule-based scan configurations and regular expressions. There is no flaky AI detection or false security reports—your scan results are exact, transparent, and reproducible.
          </p>
        </div>

        <div className="cyber-card hover:-translate-y-1 duration-300">
          <div className="h-10 w-10 rounded-lg bg-purple-950 border border-purple-500/20 flex items-center justify-center text-purple-400 mb-4 shadow-md shadow-purple-500/10">
            <Star className="h-5 w-5" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Gemini AI Explanations</h3>
          <p className="text-sm text-slate-400 leading-relaxed font-sans">
            Instead of confusing CVE vulnerability logs, Gemini translates each alert into simple, encouraging, student-friendly explanations, helping you learn and write cleaner code.
          </p>
        </div>

        <div className="cyber-card hover:-translate-y-1 duration-300">
          <div className="h-10 w-10 rounded-lg bg-emerald-950 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-4 shadow-md shadow-emerald-500/10">
            <BookOpen className="h-5 w-5" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">CS Student Friendly</h3>
          <p className="text-sm text-slate-400 leading-relaxed font-sans">
            SecureRepo flags beginner mistakes like hardcoded local system directories, merge conflict tags, and exposed server debugging flags, guiding you before you turn in homework.
          </p>
        </div>
      </div>

      {/* Pitch footer */}
      <div className="border-t border-cyber-border/40 pt-12 text-center max-w-2xl mx-auto space-y-4">
        <h4 className="text-base font-bold text-white">Join SecureRepo for Full History</h4>
        <p className="text-xs text-slate-400 leading-relaxed font-sans">
          Scanning works anonymously for a quick check. Creating a free account lets you save scans to your Dashboard, monitor progress, build a security history, and show recruiters your clean sheets!
        </p>
      </div>
    </div>
  );
}
