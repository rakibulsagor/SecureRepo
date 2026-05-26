import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Shield, Mail, Lock, AlertCircle, RefreshCw } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login, loginWithGoogle, isMockAuth } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to log in. Check your email and password.');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setError('');
    setLoading(true);

    try {
      await loginWithGoogle();
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      setError(err.message || 'Failed to sign in with Google.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto my-16 px-4">
      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-purple-600/20 rounded-2xl blur opacity-50 group-focus-within:opacity-75 transition-opacity"></div>
        
        <div className="relative cyber-card bg-cyber-card border-cyber-border rounded-2xl p-8 space-y-6">
          <div className="text-center space-y-2">
            <Link to="/" className="inline-flex items-center gap-1.5 text-2xl font-black text-cyan-400">
              <Shield className="h-6 w-6 text-cyan-400 stroke-[2] drop-shadow-[0_0_6px_rgba(0,240,255,0.5)]" />
              <span>Secure<span className="text-white">Repo</span></span>
            </Link>
            <h3 className="text-xl font-bold text-white pt-2">Welcome Back</h3>
            <p className="text-xs text-slate-400">Log in to manage your repository scans.</p>
          </div>

          {isMockAuth && (
            <div className="bg-amber-950/20 border border-amber-500/20 rounded-lg p-3 text-[11px] text-amber-400 text-center">
              💡 <strong>Demo Mode Active:</strong> You can enter any email/password to sign in locally!
            </div>
          )}

          {error && (
            <div className="bg-red-950/20 border border-red-500/20 rounded-lg p-3 text-xs text-red-400 flex items-start gap-2">
              <AlertCircle className="h-4.5 w-4.5 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Email Address</label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-500">
                  <Mail className="h-4 w-4" />
                </span>
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="name@university.edu"
                  className="cyber-input pl-10"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-bold text-slate-400 uppercase tracking-wider">Password</label>
              <div className="relative">
                <span className="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-500">
                  <Lock className="h-4 w-4" />
                </span>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="••••••••"
                  className="cyber-input pl-10"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="cyber-btn-primary w-full flex items-center justify-center gap-2 mt-2 py-3"
            >
              {loading ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          <div className="flex items-center gap-3">
            <div className="h-px flex-1 bg-slate-800/80"></div>
            <span className="text-[11px] uppercase tracking-wider text-slate-500">or</span>
            <div className="h-px flex-1 bg-slate-800/80"></div>
          </div>

          <button
            type="button"
            onClick={handleGoogleLogin}
            disabled={loading}
            className="w-full flex items-center justify-center gap-3 rounded-lg border border-slate-700 bg-slate-950/40 px-4 py-3 text-sm font-semibold text-slate-100 transition-colors hover:border-cyan-500/50 hover:bg-slate-900 disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading ? (
              <RefreshCw className="h-4 w-4 animate-spin" />
            ) : (
              <>
                <span className="flex h-5 w-5 items-center justify-center rounded-full bg-white text-sm font-black text-slate-900">G</span>
                Continue with Google
              </>
            )}
          </button>

          <div className="border-t border-slate-800/60 pt-4 text-center text-xs text-slate-400">
            Don't have an account?{' '}
            <Link to="/register" className="text-cyan-400 hover:text-cyan-300 font-semibold hover:underline">
              Create an account
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
