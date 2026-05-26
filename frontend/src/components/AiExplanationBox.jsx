import React from 'react';
import { Sparkles, Terminal, BookOpen } from 'lucide-react';

export default function AiExplanationBox({ aiSummary }) {
  if (!aiSummary) return null;

  return (
    <div className="relative group">
      {/* Glow outer border */}
      <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-xl blur opacity-75 group-hover:opacity-100 transition-opacity duration-300"></div>
      
      <div className="relative cyber-card border-cyan-500/30 bg-cyber-card/90 overflow-hidden">
        {/* Decorative corner indicator */}
        <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/5 rounded-full blur-xl pointer-events-none"></div>

        <div className="flex items-start gap-4">
          {/* Avatar Icon */}
          <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center text-white flex-shrink-0 shadow-lg shadow-cyan-500/20">
            <Sparkles className="h-5 w-5 animate-pulse" />
          </div>

          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <h4 className="text-base font-bold text-cyan-400">Security Mentor's Summary</h4>
              <span className="text-[10px] text-slate-500 bg-slate-800 px-1.5 py-0.5 rounded font-mono">Gemini AI</span>
            </div>
            
            <p className="text-sm text-slate-300 leading-relaxed font-sans font-medium">
              {aiSummary}
            </p>
            
            <div className="pt-2 flex items-center gap-4 text-xs text-slate-400">
              <span className="flex items-center gap-1">
                <BookOpen className="h-3.5 w-3.5 text-cyan-400/80" />
                Beginner-friendly advice
              </span>
              <span className="flex items-center gap-1">
                <Terminal className="h-3.5 w-3.5 text-purple-400/80" />
                Actionable next steps
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
