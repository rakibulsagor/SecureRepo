import React from 'react';

export default function SeverityBadge({ severity }) {
  const getBadgeStyles = (sev) => {
    switch (sev) {
      case 'Critical':
        return 'bg-red-500/10 text-red-400 border-red-500/20';
      case 'High':
        return 'bg-orange-500/10 text-orange-400 border-orange-500/20';
      case 'Medium':
        return 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20';
      case 'Low':
        return 'bg-green-500/10 text-green-400 border-green-500/20';
      default:
        return 'bg-slate-800 text-slate-400 border-slate-700';
    }
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getBadgeStyles(severity)}`}>
      {severity}
    </span>
  );
}
