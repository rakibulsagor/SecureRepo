import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  ShieldAlert, ShieldCheck, History, Search, 
  BarChart3, RefreshCw, AlertTriangle, PlusCircle 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { scanApi } from '../api/scanApi';
import ScanHistoryCard from '../components/ScanHistoryCard';
import RepoInput from '../components/RepoInput';
import LoadingScan from '../components/LoadingScan';

export default function Dashboard() {
  const { currentUser } = useAuth();
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [scanError, setScanError] = useState('');
  const [stats, setStats] = useState({
    totalScans: 0,
    avgScore: 0,
    criticalCount: 0,
    warningCount: 0,
  });

  const navigate = useNavigate();

  const fetchScanHistory = async () => {
    try {
      setLoading(true);
      const data = await scanApi.getScanHistory(currentUser.uid);
      setScans(data);
      calculateStats(data);
    } catch (error) {
      console.error("Failed to load scan history:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (currentUser) {
      fetchScanHistory();
    }
  }, [currentUser]);

  const calculateStats = (scanList) => {
    if (!scanList || scanList.length === 0) {
      setStats({ totalScans: 0, avgScore: 0, criticalCount: 0, warningCount: 0 });
      return;
    }

    const total = scanList.length;
    const sumScore = scanList.reduce((acc, curr) => acc + curr.score, 0);
    const avg = Math.round(sumScore / total);

    let criticals = 0;
    let warnings = 0;
    scanList.forEach((scan) => {
      criticals += (scan.issueCounts.critical || 0);
      warnings += (scan.issueCounts.high || 0) + (scan.issueCounts.medium || 0);
    });

    setStats({
      totalScans: total,
      avgScore: avg,
      criticalCount: criticals,
      warningCount: warnings
    });
  };

  const handleScan = async (repoUrl, useAi) => {
    setScanning(true);
    setScanError('');
    try {
      const scanResult = await scanApi.runScan(repoUrl, currentUser.uid, useAi);
      setTimeout(() => {
        navigate(`/report/${scanResult.scan_id}`);
      }, 500);
    } catch (err) {
      console.error(err);
      const errMsg = err.response?.data?.detail || 'Scan failed. Make sure the repository is public and git is installed.';
      setScanError(errMsg);
      setScanning(false);
    }
  };

  const handleDeleteScan = async (scanId) => {
    try {
      await scanApi.deleteScan(scanId);
      const updated = scans.filter((s) => s.scanId !== scanId);
      setScans(updated);
      calculateStats(updated);
    } catch (error) {
      console.error("Failed to delete scan:", error);
      alert("Failed to delete scan. Try again.");
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-400';
    if (score >= 75) return 'text-emerald-400';
    if (score >= 50) return 'text-yellow-400';
    return 'text-red-400';
  };

  if (scanning) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <LoadingScan />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      {/* Welcome Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-cyber-border/40 pb-6">
        <div>
          <h2 className="text-3xl font-extrabold text-white">
            Welcome back, {currentUser.displayName}!
          </h2>
          <p className="text-sm text-slate-400">
            Monitor and secure your codebases using deterministic security scans.
          </p>
        </div>
      </div>

      {/* Stats Widgets */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="cyber-card flex items-center gap-4 bg-cyber-card/60">
          <div className="h-12 w-12 rounded-lg bg-cyan-950/40 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
            <BarChart3 className="h-6 w-6" />
          </div>
          <div>
            <span className="block text-xs text-slate-400 uppercase font-bold tracking-wider">Total Scans</span>
            <span className="text-2xl font-black text-white">{stats.totalScans}</span>
          </div>
        </div>

        <div className="cyber-card flex items-center gap-4 bg-cyber-card/60">
          <div className="h-12 w-12 rounded-lg bg-indigo-950/40 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
            <ShieldCheck className="h-6 w-6" />
          </div>
          <div>
            <span className="block text-xs text-slate-400 uppercase font-bold tracking-wider">Avg Security Score</span>
            <span className={`text-2xl font-black ${getScoreColor(stats.avgScore)}`}>
              {stats.avgScore === 0 && scans.length === 0 ? '—' : `${stats.avgScore}/100`}
            </span>
          </div>
        </div>

        <div className="cyber-card flex items-center gap-4 bg-cyber-card/60">
          <div className="h-12 w-12 rounded-lg bg-red-950/40 border border-red-500/20 flex items-center justify-center text-red-400">
            <ShieldAlert className="h-6 w-6" />
          </div>
          <div>
            <span className="block text-xs text-slate-400 uppercase font-bold tracking-wider">Active Criticals</span>
            <span className="text-2xl font-black text-white">{stats.criticalCount}</span>
          </div>
        </div>

        <div className="cyber-card flex items-center gap-4 bg-cyber-card/60">
          <div className="h-12 w-12 rounded-lg bg-yellow-950/40 border border-yellow-500/20 flex items-center justify-center text-yellow-400">
            <AlertTriangle className="h-6 w-6" />
          </div>
          <div>
            <span className="block text-xs text-slate-400 uppercase font-bold tracking-wider">High/Med Warnings</span>
            <span className="text-2xl font-black text-white">{stats.warningCount}</span>
          </div>
        </div>
      </div>

      {/* New Scan panel */}
      <div className="cyber-card border-cyan-500/10 bg-cyber-dark/40 p-6 space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <PlusCircle className="h-5 w-5 text-cyan-400" />
          Scan a New Repository
        </h3>
        <RepoInput onScan={handleScan} isLoading={scanning} />
        {scanError && (
          <div className="p-4 bg-red-950/20 border border-red-500/20 text-red-400 rounded-xl text-sm">
            {scanError}
          </div>
        )}
      </div>

      {/* Scans List */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          <History className="h-5 w-5 text-slate-400" />
          Scan History
        </h3>

        {loading ? (
          <div className="flex justify-center items-center py-16">
            <RefreshCw className="h-8 w-8 text-cyan-400 animate-spin" />
          </div>
        ) : scans.length === 0 ? (
          <div className="text-center py-16 cyber-card bg-cyber-card/25 border-dashed">
            <ShieldAlert className="h-12 w-12 text-slate-500 mx-auto mb-3" />
            <h4 className="text-base font-bold text-white mb-1">No Scans Found</h4>
            <p className="text-sm text-slate-400 max-w-sm mx-auto mb-6">
              You haven't run any repository scans under this account yet. Scan a project above to get started!
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {scans.map((scan) => (
              <ScanHistoryCard 
                key={scan.scanId} 
                scan={scan} 
                onDelete={handleDeleteScan} 
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
