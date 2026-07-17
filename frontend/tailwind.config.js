/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        // Section 15.2 palette, expressed as a full scale for each role.
        primary: {
          50: "#eff6ff", 100: "#dbeafe", 200: "#bfdbfe", 300: "#93c5fd",
          400: "#60a5fa", 500: "#3b82f6", 600: "#2563eb", 700: "#1d4ed8",
          800: "#1e40af", 900: "#1e3a8a",
        },
        success: { 50: "#f0fdf4", 100: "#dcfce7", 500: "#22c55e", 600: "#16a34a", 700: "#15803d" },
        warning: { 50: "#fffbeb", 100: "#fef3c7", 500: "#f59e0b", 600: "#d97706", 700: "#b45309" },
        critical: { 50: "#fef2f2", 100: "#fee2e2", 500: "#ef4444", 600: "#dc2626", 700: "#b91c1c" },
        surface: "#ffffff",
        "surface-secondary": "#f4f5f7",
        ink: {
          900: "#0f172a", 700: "#334155", 500: "#64748b", 300: "#cbd5e1", 100: "#e2e8f0",
        },
      },
      fontFamily: {
        display: ["'Sora'", "system-ui", "sans-serif"],
        body: ["'IBM Plex Sans'", "system-ui", "sans-serif"],
        mono: ["'IBM Plex Mono'", "ui-monospace", "monospace"],
      },
      boxShadow: {
        card: "0 1px 2px rgba(15, 23, 42, 0.06), 0 1px 3px rgba(15, 23, 42, 0.08)",
      },
    },
  },
  plugins: [],
};
