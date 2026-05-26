import React, { useState } from 'react';
import { AlertCircle, Code, FileText, ChevronDown, ChevronUp, Sparkles, RefreshCw } from 'lucide-react';
import SeverityBadge from './SeverityBadge';
import { scanApi } from '../api/scanApi';

export default function IssueCard({ issue }) {
  const [isOpen, setIsOpen] = useState(false);
  const [explanation, setExplanation] = useState(issue.studentExplanation);
  const [loadingAi, setLoadingAi] = useState(false);

  const getLeftBorder = (sev) => {
    switch (sev) {
      case 'Critical': return 'border-l-4 border-l-red-500';
      case 'High': return 'border-l-4 border-l-orange-500';
      case 'Medium': return 'border-l-4 border-l-yellow-500';
      case 'Low': return 'border-l-4 border-l-green-500';
      default: return 'border-l-4 border-l-slate-700';
    }
  };

  const handleFetchAiExplanation = async (e) => {
    e.stopPropagation(); // Avoid closing the accordion
    setLoadingAi(true);
    try {
      const res = await scanApi.explainIssue(issue.issue_id);
      setExplanation(res.explanation);
      setIsOpen(true);
    } catch (error) {
      console.error("Failed to fetch AI explanation:", error);
    } finally {
      setLoadingAi(false);
    }
  };

  return (
    <div className={`cyber-card bg-cyber-card/90 ${getLeftBorder(issue.severity)} hover:bg-cyber-card transition-all duration-200 overflow-hidden`}>
      {/* Card Header (Clickable to toggle details) */}
      <div 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-start justify-between gap-4 cursor-pointer select-none"
      >
        <div className="flex-1 space-y-1.5">
          <div className="flex flex-wrap items-center gap-2">
            <SeverityBadge severity={issue.severity} />
            <span className="text-xs font-semibold text-slate-400 bg-slate-800/40 border border-slate-700/50 px-2 py-0.5 rounded">
              {issue.type}
            </span>
            <span className="text-xs text-slate-500 flex items-center gap-1 font-mono">
              <FileText className="h-3 w-3" />
              {issue.file} {issue.line ? `(Line ${issue.line})` : ''}
            </span>
          </div>
          <h4 className="text-base font-bold text-white leading-snug">
            {issue.message}
          </h4>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0 text-slate-400">
          {!explanation && (
            <button
              onClick={handleFetchAiExplanation}
              disabled={loadingAi}
              className="flex items-center gap-1 bg-cyan-950/40 text-cyan-400 border border-cyan-800/30 hover:border-cyan-500 hover:bg-cyan-950/60 transition-all rounded px-2.5 py-1 text-xs"
            >
              {loadingAi ? (
                <RefreshCw className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <Sparkles className="h-3.5 w-3.5" />
              )}
              <span>Ask AI</span>
            </button>
          )}
          <div className="hover:text-white p-1">
            {isOpen ? <ChevronUp className="h-5 w-5" /> : <ChevronDown className="h-5 w-5" />}
          </div>
        </div>
      </div>

      {/* Expandable Details */}
      {isOpen && (
        <div className="mt-5 pt-4 border-t border-slate-800/60 space-y-4">
          {/* Fix recommendation */}
          <div className="space-y-1.5">
            <h5 className="text-xs font-bold text-slate-400 flex items-center gap-1 uppercase tracking-wider">
              <Code className="h-3.5 w-3.5 text-slate-400" />
              How to Fix
            </h5>
            <div className="bg-cyber-darkest border border-cyber-border rounded-lg p-3 text-sm text-slate-300 font-mono overflow-x-auto">
              {issue.fix}
            </div>
          </div>

          {/* AI Explanation Box */}
          {explanation && (
            <div className="bg-cyan-950/10 border border-cyan-800/20 rounded-lg p-4 space-y-2 relative overflow-hidden">
              {/* Background gradient hint */}
              <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/5 rounded-full blur-xl pointer-events-none"></div>
              
              <h5 className="text-xs font-bold text-cyan-400 flex items-center gap-1 uppercase tracking-wider select-none">
                <Sparkles className="h-3.5 w-3.5" />
                Teacher's Explanation (Gemini AI)
              </h5>
              <p className="text-sm text-slate-300 leading-relaxed font-sans">
                {explanation}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
