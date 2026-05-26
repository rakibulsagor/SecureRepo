import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, Trash2, ArrowRight, ShieldAlert, Github } from 'lucide-react';

export default function ScanHistoryCard({ scan, onDelete }) {
  const navigate = useNavigate();

  const getScoreColor = (val) => {
    if (val >= 90) return 'text-green-400 bg-green-950/20 border-green-500/30';
    if (val >= 75) return 'text-emerald-400 bg-emerald-950/20 border-emerald-500/30';
    if (val >= 50) return 'text-yellow-400 bg-yellow-950/20 border-yellow-500/30';
    if (val >= 25) return 'text-orange-400 bg-orange-950/20 border-orange-500/30';
    return 'text-red-400 bg-red-950/20 border-red-500/30';
  };

  const formatDate = (isoString) => {
    if (!isoString) return 'Unknown date';
    try {
      const date = new Date(isoString);
      return date.toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return isoString;
    }
  };

  const handleCardClick = () => {
    navigate(`/report/${scan.scanId}`);
  };

  const handleDelete = (e) => {
    e.stopPropagation(); // Avoid navigating
    if (window.confirm("Are you sure you want to delete this scan from your history?")) {
      onDelete(scan.scanId);
    }
  };

  return (
    <div 
      onClick={handleCardClick}
      className="cyber-card-glow cursor-pointer relative group flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 bg-cyber-card/75"
    >
      {/* Repo details and Date */}
      <div className="flex-1 space-y-2">
        <div className="flex items-center gap-2">
          <div className="h-7 w-7 rounded bg-slate-800 flex items-center justify-center text-slate-300">
            <Github className="h-4 w-4" />
          </div>
          <span className="font-bold text-white text-base leading-tight">
            {scan.owner}/{scan.repoName}
          </span>
        </div>
        
        <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-xs text-slate-400">
          <span className="flex items-center gap-1">
            <Calendar className="h-3.5 w-3.5" />
            {formatDate(scan.createdAt)}
          </span>
          <span className="flex items-center gap-1.5 text-slate-300">
            <ShieldAlert className="h-3.5 w-3.5 text-cyan-400" />
            {scan.issueCounts.critical + scan.issueCounts.high + scan.issueCounts.medium + scan.issueCounts.low} issues found
          </span>
        </div>

        {/* Small issues list */}
        <div className="flex gap-2.5 pt-1 text-[10px] font-semibold text-slate-400">
          {scan.issueCounts.critical > 0 && <span className="bg-red-950/20 text-red-400 border border-red-500/10 px-1.5 py-0.5 rounded">Crit: {scan.issueCounts.critical}</span>}
          {scan.issueCounts.high > 0 && <span className="bg-orange-950/20 text-orange-400 border border-orange-500/10 px-1.5 py-0.5 rounded">High: {scan.issueCounts.high}</span>}
          {scan.issueCounts.medium > 0 && <span className="bg-yellow-950/20 text-yellow-400 border border-yellow-500/10 px-1.5 py-0.5 rounded">Med: {scan.issueCounts.medium}</span>}
          {scan.issueCounts.low > 0 && <span className="bg-green-950/20 text-green-400 border border-green-500/10 px-1.5 py-0.5 rounded">Low: {scan.issueCounts.low}</span>}
        </div>
      </div>

      {/* Score and actions */}
      <div className="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end border-t border-slate-800/40 md:border-t-0 pt-3 md:pt-0">
        <div className={`px-4 py-2 rounded-lg border text-center ${getScoreColor(scan.score)}`}>
          <span className="block text-2xl font-black leading-none">{scan.score}</span>
          <span className="text-[8px] font-bold uppercase tracking-wider mt-0.5 block">{scan.riskLevel}</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleDelete}
            className="p-2 text-slate-500 hover:text-red-400 hover:bg-red-950/20 rounded border border-transparent hover:border-red-500/20 transition-all"
            title="Delete Scan"
          >
            <Trash2 className="h-4 w-4" />
          </button>
          
          <div className="p-2 bg-slate-800 group-hover:bg-cyan-600 group-hover:text-white text-slate-300 rounded transition-all">
            <ArrowRight className="h-4 w-4" />
          </div>
        </div>
      </div>
    </div>
  );
}
