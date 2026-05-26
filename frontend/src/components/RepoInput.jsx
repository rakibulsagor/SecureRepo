import React, { useState } from 'react';
import { Search, Github, AlertTriangle, Sparkles, Folder } from 'lucide-react';

export default function RepoInput({ onScan, isLoading }) {
  const [repoUrl, setRepoUrl] = useState('');
  const [useAi, setUseAi] = useState(true);
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    const trimmed = repoUrl.trim();
    if (!trimmed) {
      setError('Please enter a repository URL or local path.');
      return;
    }

    onScan(trimmed, useAi);
  };

  const loadExample = (url) => {
    setRepoUrl(url);
    setError('');
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-xl blur opacity-25 group-focus-within:opacity-50 transition-opacity duration-300"></div>
          <div className="relative flex items-center bg-cyber-card border border-cyber-border rounded-xl p-1.5 focus-within:border-cyan-500 transition-all duration-300">
            <div className="pl-3 text-slate-400">
              <Github className="h-5 w-5" />
            </div>
            <input
              type="text"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              disabled={isLoading}
              placeholder="https://github.com/owner/repository  or  local folder path..."
              className="w-full bg-transparent border-0 focus:outline-none focus:ring-0 text-slate-100 placeholder-slate-500 px-3 py-3 text-base"
            />
            <button
              type="submit"
              disabled={isLoading}
              className="cyber-btn-primary flex items-center gap-1.5 px-6 py-3"
            >
              <Search className="h-4 w-4" />
              <span>Scan Repo</span>
            </button>
          </div>
        </div>

        {error && (
          <div className="flex items-center gap-2 text-red-400 text-sm px-1.5">
            <AlertTriangle className="h-4 w-4" />
            <span>{error}</span>
          </div>
        )}

        <div className="flex flex-wrap items-center justify-between gap-4 px-1.5 text-xs text-slate-400">
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={useAi}
              onChange={(e) => setUseAi(e.target.checked)}
              disabled={isLoading}
              className="rounded bg-cyber-dark border-cyber-border text-cyan-500 focus:ring-cyan-500 focus:ring-offset-cyber-darkest h-4 w-4"
            />
            <span className="flex items-center gap-1 text-slate-300">
              <Sparkles className="h-3 w-3 text-cyan-400" />
              Enable Gemini AI explanations
            </span>
          </label>

          <div className="flex items-center gap-2">
            <span>Examples:</span>
            <button
              type="button"
              onClick={() => loadExample('demo-vulnerable-repo')}
              className="text-cyan-400 hover:text-cyan-300 border border-cyan-800/30 bg-cyan-950/20 px-2 py-0.5 rounded transition-all hover:bg-cyan-950/40 flex items-center gap-0.5"
            >
              <Folder className="h-2.5 w-2.5" />
              Local Demo Repo
            </button>
            <button
              type="button"
              onClick={() => loadExample('https://github.com/expressjs/express')}
              className="text-slate-300 hover:text-white border border-slate-700 bg-slate-800/30 px-2 py-0.5 rounded transition-all"
            >
              Express (Public)
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
