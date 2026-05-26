import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft, Github, AlertTriangle, ShieldCheck, 
  Cpu, ListFilter, RefreshCw 
} from 'lucide-react';
import { scanApi } from '../api/scanApi';
import ScoreCard from '../components/ScoreCard';
import IssueCard from '../components/IssueCard';
import SoftwareVersionTable from '../components/SoftwareVersionTable';
import AiExplanationBox from '../components/AiExplanationBox';

export default function Report() {
  const { scanId } = useParams();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('issues'); // issues | runtimes

  useEffect(() => {
    const fetchReport = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await scanApi.getScanDetails(scanId);
        setReport(data);
      } catch (err) {
        console.error("Error fetching report:", err);
        setError(err.response?.data?.detail || "Failed to load report details. Make sure this scan exists.");
      } finally {
        setLoading(false);
      }
    };

    if (scanId) {
      fetchReport();
    }
  }, [scanId]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-32 space-y-4">
        <RefreshCw className="h-10 w-10 text-cyan-400 animate-spin" />
        <span className="text-slate-400 text-sm">Loading security report...</span>
      </div>
    );
  }

  if (error || !report) {
    return (
      <div className="max-w-3xl mx-auto my-16 px-4">
        <div className="cyber-card border-red-500/20 bg-red-950/5 text-center p-8 space-y-4">
          <AlertTriangle className="h-12 w-12 text-red-500 mx-auto" />
          <h3 className="text-xl font-bold text-white">Report Loading Failed</h3>
          <p className="text-sm text-slate-400 max-w-md mx-auto">{error}</p>
          <div className="pt-4">
            <Link to="/dashboard" className="cyber-btn-secondary inline-flex items-center gap-1.5">
              <ArrowLeft className="h-4 w-4" />
              Back to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Back button and title header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-cyber-border/40 pb-6">
        <div className="space-y-2">
          <Link 
            to="/dashboard" 
            className="inline-flex items-center gap-1 text-xs font-semibold text-slate-400 hover:text-cyan-400 transition-colors"
          >
            <ArrowLeft className="h-3 w-3" />
            Back to Dashboard
          </Link>
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-lg bg-slate-800 flex items-center justify-center text-slate-300">
              <Github className="h-5 w-5" />
            </div>
            <h2 className="text-3xl font-extrabold text-white">
              {report.repo.owner}/{report.repo.name}
            </h2>
          </div>
          <p className="text-xs text-slate-400 font-mono">
            URL: <a href={report.repo.url} target="_blank" rel="noopener noreferrer" className="text-cyan-400 hover:underline">{report.repo.url}</a>
          </p>
        </div>
      </div>

      {/* Main Score Summary & AI Mentor Box */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <div className="lg:col-span-2">
          <ScoreCard 
            score={report.score} 
            riskLevel={report.risk_level} 
            summary={report.summary} 
          />
        </div>
        <div>
          <AiExplanationBox aiSummary={report.ai_summary} />
        </div>
      </div>

      {/* Tabs list */}
      <div className="space-y-6">
        <div className="flex border-b border-cyber-border/60">
          <button
            onClick={() => setActiveTab('issues')}
            className={`flex items-center gap-2 px-6 py-3 font-semibold text-sm transition-colors border-b-2 ${
              activeTab === 'issues' 
                ? 'text-cyan-400 border-cyan-400 bg-cyan-950/10' 
                : 'text-slate-400 hover:text-white border-transparent hover:bg-slate-800/20'
            }`}
          >
            <ListFilter className="h-4 w-4" />
            Vulnerabilities ({report.issues.length})
          </button>
          
          <button
            onClick={() => setActiveTab('runtimes')}
            className={`flex items-center gap-2 px-6 py-3 font-semibold text-sm transition-colors border-b-2 ${
              activeTab === 'runtimes' 
                ? 'text-cyan-400 border-cyan-400 bg-cyan-950/10' 
                : 'text-slate-400 hover:text-white border-transparent hover:bg-slate-800/20'
            }`}
          >
            <Cpu className="h-4 w-4" />
            Software Runtimes
          </button>
        </div>

        {/* Tab content panels */}
        <div className="pt-2">
          {activeTab === 'issues' && (
            <div className="space-y-4">
              {report.issues.length === 0 ? (
                <div className="text-center py-16 cyber-card bg-emerald-950/5 border-emerald-500/20 text-emerald-400">
                  <ShieldCheck className="h-12 w-12 mx-auto mb-3 text-emerald-400" />
                  <h4 className="text-lg font-bold text-white mb-1">Codebase Secure!</h4>
                  <p className="text-sm text-slate-400 max-w-sm mx-auto">
                    We didn't detect any hardcoded keys, configuration flaws, or beginner security issues. Excellent code hygiene!
                  </p>
                </div>
              ) : (
                report.issues.map((issue) => (
                  <IssueCard key={issue.issue_id} issue={issue} />
                ))
              )}
            </div>
          )}

          {activeTab === 'runtimes' && (
            <SoftwareVersionTable softwareList={report.detected_software} />
          )}
        </div>
      </div>
    </div>
  );
}
