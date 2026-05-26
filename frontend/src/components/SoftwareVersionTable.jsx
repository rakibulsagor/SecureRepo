import React from 'react';
import { AlertCircle, CheckCircle, HelpCircle } from 'lucide-react';

export default function SoftwareVersionTable({ softwareList }) {
  if (!softwareList || softwareList.length === 0) {
    return (
      <div className="text-center py-6 text-sm text-slate-500 border border-dashed border-cyber-border rounded-lg">
        No runtime engines detected.
      </div>
    );
  }

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Secure':
        return (
          <span className="inline-flex items-center gap-1 text-xs font-semibold text-green-400 bg-green-950/20 border border-green-500/20 px-2 py-0.5 rounded-full">
            <CheckCircle className="h-3 w-3" />
            Secure
          </span>
        );
      case 'Outdated':
        return (
          <span className="inline-flex items-center gap-1 text-xs font-semibold text-red-400 bg-red-950/20 border border-red-500/20 px-2 py-0.5 rounded-full">
            <AlertCircle className="h-3 w-3" />
            Outdated
          </span>
        );
      case 'Warning':
        return (
          <span className="inline-flex items-center gap-1 text-xs font-semibold text-yellow-400 bg-yellow-950/20 border border-yellow-500/20 px-2 py-0.5 rounded-full">
            <AlertCircle className="h-3 w-3" />
            Warning
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-xs font-semibold text-slate-400 bg-slate-900 border border-slate-700 px-2 py-0.5 rounded-full">
            <HelpCircle className="h-3 w-3" />
            Unknown
          </span>
        );
    }
  };

  return (
    <div className="overflow-x-auto border border-cyber-border rounded-lg bg-cyber-darkest/40">
      <table className="min-w-full divide-y divide-cyber-border text-sm">
        <thead className="bg-cyber-card/50 text-slate-400 text-left">
          <tr>
            <th className="px-4 py-3 font-semibold">Runtime / Engine</th>
            <th className="px-4 py-3 font-semibold">Type</th>
            <th className="px-4 py-3 font-semibold">Detected Version</th>
            <th className="px-4 py-3 font-semibold">Status</th>
            <th className="px-4 py-3 font-semibold text-right">Target Version</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-cyber-border/40 text-slate-300">
          {softwareList.map((sw, index) => (
            <tr key={index} className="hover:bg-slate-800/10 transition-colors">
              <td className="px-4 py-3 font-bold text-white">{sw.name}</td>
              <td className="px-4 py-3">
                <span className="text-xs font-mono text-indigo-400 bg-indigo-950/20 border border-indigo-500/15 px-2 py-0.5 rounded">
                  {sw.type}
                </span>
              </td>
              <td className="px-4 py-3 font-mono">{sw.version}</td>
              <td className="px-4 py-3">{getStatusBadge(sw.status)}</td>
              <td className="px-4 py-3 text-right font-mono text-slate-400">
                {sw.latest_stable || '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
