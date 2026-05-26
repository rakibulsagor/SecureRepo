import React from 'react';
import { AlertCircle, Shield, ShieldCheck, ShieldAlert } from 'lucide-react';

export default function ScoreCard({ score, riskLevel, summary }) {
  // Get color configurations based on score
  const getScoreTheme = (val) => {
    if (val >= 90) return {
      border: 'border-emerald-500/30',
      text: 'text-emerald-400',
      bg: 'bg-emerald-950/10',
      glow: 'shadow-glow-green',
      icon: <ShieldCheck className="h-8 w-8 text-emerald-400" />
    };
    if (val >= 75) return {
      border: 'border-green-500/30',
      text: 'text-green-400',
      bg: 'bg-green-950/10',
      glow: 'shadow-glow-green',
      icon: <Shield className="h-8 w-8 text-green-400" />
    };
    if (val >= 50) return {
      border: 'border-yellow-500/30',
      text: 'text-yellow-400',
      bg: 'bg-yellow-950/10',
      glow: 'shadow-glow-cyan',
      icon: <AlertCircle className="h-8 w-8 text-yellow-400" />
    };
    if (val >= 25) return {
      border: 'border-orange-500/30',
      text: 'text-orange-400',
      bg: 'bg-orange-950/10',
      glow: 'shadow-glow-red',
      icon: <ShieldAlert className="h-8 w-8 text-orange-400" />
    };
    return {
      border: 'border-red-500/30',
      text: 'text-red-400',
      bg: 'bg-red-950/10',
      glow: 'shadow-glow-red',
      icon: <ShieldAlert className="h-8 w-8 text-red-400" />
    };
  };

  const theme = getScoreTheme(score);

  return (
    <div className={`cyber-card ${theme.border} ${theme.bg} ${theme.glow} flex flex-col md:flex-row items-center gap-6 p-8 relative overflow-hidden`}>
      {/* Visual background details */}
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-32 h-32 rounded-full bg-cyan-500/5 blur-2xl"></div>

      {/* Score circle */}
      <div className="relative flex items-center justify-center h-32 w-32 flex-shrink-0">
        <svg className="absolute w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r="44"
            className="stroke-slate-800"
            strokeWidth="8"
            fill="transparent"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r="44"
            className={`stroke-current ${theme.text}`}
            strokeWidth="8"
            fill="transparent"
            strokeDasharray={276}
            strokeDashoffset={276 - (276 * score) / 100}
            strokeLinecap="round"
          />
        </svg>
        <div className="flex flex-col items-center">
          <span className="text-4xl font-extrabold text-white leading-none">{score}</span>
          <span className="text-[10px] text-slate-400 tracking-wider font-semibold uppercase mt-1">Score</span>
        </div>
      </div>

      {/* Summary data */}
      <div className="flex-1 text-center md:text-left">
        <div className="flex flex-col md:flex-row md:items-center gap-2 mb-2 justify-center md:justify-start">
          {theme.icon}
          <div>
            <h4 className="text-2xl font-bold text-white leading-tight">Security Rating</h4>
            <div className="flex items-center gap-2 mt-0.5 justify-center md:justify-start">
              <span className={`text-sm font-semibold ${theme.text}`}>{riskLevel}</span>
              <span className="text-xs text-slate-500">•</span>
              <span className="text-xs text-slate-400">Rule-based assessment</span>
            </div>
          </div>
        </div>
        
        {/* Severity Count Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6">
          <div className="bg-cyber-darkest/60 border border-red-500/10 rounded-lg p-2.5 text-center">
            <span className="block text-xs text-slate-400 mb-0.5">Critical</span>
            <span className={`text-lg font-bold ${summary.critical > 0 ? 'text-red-400' : 'text-slate-500'}`}>
              {summary.critical}
            </span>
          </div>
          <div className="bg-cyber-darkest/60 border border-orange-500/10 rounded-lg p-2.5 text-center">
            <span className="block text-xs text-slate-400 mb-0.5">High</span>
            <span className={`text-lg font-bold ${summary.high > 0 ? 'text-orange-400' : 'text-slate-500'}`}>
              {summary.high}
            </span>
          </div>
          <div className="bg-cyber-darkest/60 border border-yellow-500/10 rounded-lg p-2.5 text-center">
            <span className="block text-xs text-slate-400 mb-0.5">Medium</span>
            <span className={`text-lg font-bold ${summary.medium > 0 ? 'text-yellow-400' : 'text-slate-500'}`}>
              {summary.medium}
            </span>
          </div>
          <div className="bg-cyber-darkest/60 border border-green-500/10 rounded-lg p-2.5 text-center">
            <span className="block text-xs text-slate-400 mb-0.5">Low</span>
            <span className={`text-lg font-bold ${summary.low > 0 ? 'text-green-400' : 'text-slate-500'}`}>
              {summary.low}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
