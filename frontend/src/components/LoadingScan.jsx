import React, { useState, useEffect } from 'react';
import { ShieldAlert, Terminal, Loader2 } from 'lucide-react';

const SCAN_STEPS = [
  "Resolving repository URL parameters...",
  "Cloning repository using anonymous shallow checkout...",
  "Walking codebase directory structure...",
  "Running rule-based Secret Scanner (scanning AWS keys, Google API tokens, SSH keypairs)...",
  "Running Risky File Scanner (checking for committed .env, databases, PEM certs)...",
  "Running Software Version Scanner (verifying Node/Python EOL versions and Docker tags)...",
  "Running Config Weakness Scanner (validating CORS configuration, Docker user contexts)...",
  "Running Beginner Mistakes Scanner (scanning for hardcoded SQLite configs and git conflict markers)...",
  "Aggregating security issues and calculating safety index...",
  "Requesting student-friendly explanations from Gemini AI...",
  "Saving report and scan telemetry to Cloud Firestore database...",
  "Finalizing scanner logs and preparing dashboard..."
];

export default function LoadingScan() {
  const [currentStep, setCurrentStep] = useState(0);
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    // Reset state
    setCurrentStep(0);
    setLogs([`[INIT] Starting SecureRepo Security Scanner v1.0.0...`]);

    const logInterval = setInterval(() => {
      setCurrentStep((prevStep) => {
        if (prevStep < SCAN_STEPS.length) {
          const timestamp = new Date().toLocaleTimeString();
          const logPrefix = prevStep >= 9 ? "[SYSTEM]" : prevStep >= 3 ? "[SCANNER]" : "[GIT]";
          const nextLog = `[${timestamp}] ${logPrefix} ${SCAN_STEPS[prevStep]}`;
          
          setLogs((prevLogs) => [...prevLogs, nextLog]);
          return prevStep + 1;
        } else {
          clearInterval(logInterval);
          return prevStep;
        }
      });
    }, 1200);

    return () => clearInterval(logInterval);
  }, []);

  return (
    <div className="w-full max-w-3xl mx-auto cyber-card border-cyan-500/20 bg-cyber-dark/50 relative overflow-hidden">
      {/* Glow highlight */}
      <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-cyan-500 to-transparent"></div>
      
      <div className="flex flex-col items-center justify-center py-8 text-center border-b border-cyber-border">
        <div className="relative mb-4">
          <Loader2 className="h-12 w-12 text-cyan-400 animate-spin" />
          <ShieldAlert className="h-6 w-6 text-cyan-400 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 animate-pulse" />
        </div>
        <h3 className="text-xl font-bold text-white mb-2">Analyzing Repository</h3>
        <p className="text-sm text-slate-400 max-w-md">
          Please wait. SecureRepo is conducting rule-based scanning on your code structure and checking with Gemini.
        </p>
      </div>

      {/* Mock Terminal Output */}
      <div className="p-4 bg-cyber-darkest rounded-b-xl border-t border-cyber-border font-mono text-xs text-slate-300">
        <div className="flex items-center gap-2 pb-2 mb-3 border-b border-slate-800/40 text-slate-400">
          <Terminal className="h-4 w-4" />
          <span>Security Console Output</span>
        </div>
        <div className="space-y-1.5 h-64 overflow-y-auto scrollbar-thin select-text">
          {logs.map((log, index) => (
            <div 
              key={index}
              className={`${
                log.includes('[INIT]') ? 'text-cyan-400 font-bold' :
                log.includes('[SCANNER]') ? 'text-indigo-300' :
                log.includes('[GIT]') ? 'text-emerald-400' :
                log.includes('[SYSTEM]') ? 'text-amber-400' : 'text-slate-300'
              }`}
            >
              {log}
            </div>
          ))}
          {currentStep < SCAN_STEPS.length && (
            <div className="text-cyan-500 flex items-center gap-1 animate-pulse">
              <span>● Running task...</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
