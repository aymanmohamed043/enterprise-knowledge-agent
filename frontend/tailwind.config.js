/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      animation: {
        "dots": "dots 1.4s ease-in-out infinite both",
      },
      keyframes: {
        dots: {
          "0%, 80%, 100%": { opacity: "0" },
          "40%": { opacity: "1" },
        },
      },
      colors: {
        background: "#0f172a",
        card: "#111827",
        border: "#1f2937",
        accent: "#38bdf8",
        "text-primary": "#e5e7eb",
        "text-muted": "#9ca3af",
      },
      boxShadow: {
        glow: "0 0 20px rgba(56, 189, 248, 0.3)",
        "glow-sm": "0 0 12px rgba(56, 189, 248, 0.2)",
      },
    },
  },
  plugins: [],
};
