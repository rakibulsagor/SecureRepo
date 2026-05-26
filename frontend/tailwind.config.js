/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          darkest: '#05070f',
          dark: '#0a0e1a',
          card: '#0f1626',
          border: '#1e293b',
          glow: '#00f0ff',
          teal: '#0ea5e9',
          purple: '#8b5cf6',
          critical: '#ef4444',
          high: '#f97316',
          medium: '#eab308',
          low: '#22c55e',
        }
      },
      boxShadow: {
        'glow-cyan': '0 0 15px rgba(0, 240, 255, 0.25)',
        'glow-red': '0 0 15px rgba(239, 68, 68, 0.25)',
        'glow-green': '0 0 15px rgba(34, 197, 94, 0.25)',
      },
      animation: {
        'pulse-fast': 'pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 3s linear infinite',
      }
    },
  },
  plugins: [],
}
