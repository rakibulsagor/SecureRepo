import React from 'react';
import { BookOpen, Star, AlertTriangle, Key, Terminal, Code, Cpu } from 'lucide-react';

export default function Learn() {
  const articles = [
    {
      title: "Why Secrets Should Never Go to GitHub",
      category: "Secrets",
      icon: <Key className="h-5 w-5 text-cyan-400" />,
      description: "Understand how API keys, AWS credentials, and private SSH keys get leaked, and how automated scrapers scan public repositories within seconds.",
      details: [
        "Automated scrapers crawl GitHub public code constantly searching for tokens.",
        "A leaked AWS key can lead to attackers launching expensive mining rigs in minutes.",
        "Deleting a key in a new commit does NOT remove it from git history—it can still be accessed via past commits."
      ],
      remedy: "Initialize a `.gitignore` immediately. Use environment variables via libraries like `dotenv` for Python or Node."
    },
    {
      title: "The Danger of Wildcard CORS (Access-Control-Allow-Origin: *)",
      category: "Configuration",
      icon: <Terminal className="h-5 w-5 text-purple-400" />,
      description: "Learn what Cross-Origin Resource Sharing (CORS) is and why using wildcard '*' settings leaves your backend APIs vulnerable to CSRF and data leakage.",
      details: [
        "CORS controls which websites can request data from your server.",
        "Using '*' allows any malicious website loaded in a user's browser to send requests to your server.",
        "If your backend authenticates users, malicious sites can pull private user data."
      ],
      remedy: "Explicitly list allowed frontend domains (e.g. `http://localhost:5173`) in your CORS policy configuration."
    },
    {
      title: "Keeping Runtimes Secure",
      category: "Updates",
      icon: <Cpu className="h-5 w-5 text-emerald-400" />,
      description: "Why keeping your runtime engines (Node, Python, Java) updated is your primary defense against CVE vulnerabilities and unsupported software risks.",
      details: [
        "Older framework and runtime versions contain known bugs logged in CVE databases.",
        "Attacking tools scan codebases for outdated runtimes to execute automated exploits.",
        "EOL (End-of-Life) engines (e.g. Python < 3.9) stop receiving critical security updates."
      ],
      remedy: "Specify explicit minimal runtime versions in Dockerfiles, runtime.txt, or .python-version, and update them regularly to stable LTS releases."
    },
    {
      title: "Running Docker Containers as Root",
      category: "Containerization",
      icon: <Code className="h-5 w-5 text-indigo-400" />,
      description: "Why leaving your Docker container running as the root user makes you susceptible to container escapes and server takeovers.",
      details: [
        "By default, if you don't declare USER in a Dockerfile, everything runs as root.",
        "If an attacker exploits a code vulnerability, they instantly have root access inside the container.",
        "Under certain configurations, root users in containers can compromise the host machine's OS kernel."
      ],
      remedy: "Create a system group and user in your Dockerfile, and switch to it using `USER` before starting your app."
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-10">
      {/* Title */}
      <div className="border-b border-cyber-border/40 pb-6">
        <h2 className="text-3xl font-extrabold text-white flex items-center gap-2">
          <BookOpen className="h-8 w-8 text-cyan-400" />
          Security Learning Hub
        </h2>
        <p className="text-sm text-slate-400">
          Learn the principles behind SecureRepo scanner rules and master codebase security.
        </p>
      </div>

      {/* Hero Tip */}
      <div className="cyber-card border-purple-500/20 bg-purple-950/10 flex items-start gap-4 p-6 relative overflow-hidden">
        <div className="h-10 w-10 bg-purple-950/50 border border-purple-500/30 rounded-lg flex items-center justify-center text-purple-400 flex-shrink-0">
          <Star className="h-5 w-5 animate-pulse" />
        </div>
        <div>
          <h4 className="text-base font-bold text-purple-300">Security Rule of Thumb</h4>
          <p className="text-sm text-slate-300 leading-relaxed mt-1">
            Never trust user input, never commit secrets to version control, run processes with the lowest possible privileges, and update runtimes regularly. Following these four pillars solves 90% of common student security flaws!
          </p>
        </div>
      </div>

      {/* Articles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {articles.map((article, idx) => (
          <div key={idx} className="cyber-card flex flex-col justify-between h-full bg-cyber-card/65">
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800/40 pb-3">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider bg-slate-800/40 px-2 py-0.5 rounded">
                  {article.category}
                </span>
                <div className="h-8 w-8 bg-slate-900 border border-slate-800 rounded flex items-center justify-center">
                  {article.icon}
                </div>
              </div>

              <div className="space-y-2">
                <h3 className="text-lg font-bold text-white hover:text-cyan-400 transition-colors">
                  {article.title}
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed font-sans">
                  {article.description}
                </p>
              </div>

              <div className="space-y-1.5 pt-2">
                <h4 className="text-xs font-bold text-slate-300">Key Risks:</h4>
                <ul className="list-disc pl-4 space-y-1 text-xs text-slate-400 leading-normal">
                  {article.details.map((detail, dIdx) => (
                    <li key={dIdx}>{detail}</li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="pt-6 mt-4 border-t border-slate-800/40 space-y-1 text-xs">
              <span className="font-bold text-cyan-400 uppercase tracking-wide">Developer Fix:</span>
              <p className="text-slate-300">{article.remedy}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
