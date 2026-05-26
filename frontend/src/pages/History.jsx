import React, { useState, useEffect } from 'react';
import { History as HistoryIcon, RefreshCw, ShieldAlert, Trash2, Search } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { scanApi } from '../api/scanApi';
import ScanHistoryCard from '../components/ScanHistoryCard';

export default function History() {
  const { currentUser } = useAuth();
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  const fetchScans = async () => {
    try {
      setLoading(true);
      const data = await scanApi.getScanHistory(currentUser.uid);
      setScans(data);
    } catch (error) {
      console.error("Failed to load history:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (currentUser) {
      fetchScans();
    }
  }, [currentUser]);

  const handleDelete = async (scanId) => {
    try {
      await scanApi.deleteScan(scanId);
      setScans(scans.filter((s) => s.scanId !== scanId));
    } catch (error) {
      console.error("Failed to delete scan:", error);
      alert("Failed to delete scan.");
    }
  };

  const filteredScans = scans.filter((scan) => {
    const term = searchQuery.toLowerCase();
    return (
      scan.repoName.toLowerCase().includes(term) ||
      scan.owner.toLowerCase().includes(term) ||
      scan.riskLevel.toLowerCase().includes(term)
    );
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-cyber-border/40 pb-6">
        <div>
          <h2 className="text-3xl font-extrabold text-white flex items-center gap-2">
            <HistoryIcon className="h-8 w-8 text-cyan-400" />
            Scan Archive
          </h2>
          <p className="text-sm text-slate-400">
            Browse and manage all historical security scans performed on your account.
          </p>
        </div>
      </div>

      {/* Filter and search bar */}
      <div className="relative group max-w-md">
        <div className="absolute inset-0 bg-cyan-500/10 rounded-lg blur opacity-50 group-focus-within:opacity-75 transition-opacity duration-300"></div>
        <div className="relative flex items-center bg-cyber-card border border-cyber-border rounded-lg p-1 focus-within:border-cyan-500">
          <div className="pl-3 text-slate-500">
            <Search className="h-4 w-4" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by repo owner, name, or risk level..."
            className="w-full bg-transparent border-0 focus:outline-none focus:ring-0 text-sm text-slate-100 placeholder-slate-500 px-3 py-2"
          />
        </div>
      </div>

      {/* History content list */}
      <div>
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <RefreshCw className="h-8 w-8 text-cyan-400 animate-spin" />
          </div>
        ) : filteredScans.length === 0 ? (
          <div className="text-center py-20 cyber-card bg-cyber-card/10 border-dashed">
            <ShieldAlert className="h-12 w-12 text-slate-500 mx-auto mb-3" />
            <h4 className="text-base font-bold text-white mb-1">
              {scans.length === 0 ? 'No Scans Run Yet' : 'No Matching Scans'}
            </h4>
            <p className="text-sm text-slate-400 max-w-sm mx-auto">
              {scans.length === 0 
                ? "You haven't run any scans under this account. Run a scan from the Home tab or Dashboard!"
                : "No results matched your search query. Try typing another repository name."}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredScans.map((scan) => (
              <ScanHistoryCard 
                key={scan.scanId} 
                scan={scan} 
                onDelete={handleDelete} 
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
