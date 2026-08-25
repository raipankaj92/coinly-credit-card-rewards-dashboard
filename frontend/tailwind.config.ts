import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      boxShadow: {
        panel: "0 12px 36px rgba(18, 26, 38, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;
