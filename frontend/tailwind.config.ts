import type { Config } from "tailwindcss";

const withMT = require("@material-tailwind/react/utils/withMT");


module.exports = withMT({
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        'primary-bg':'#2A363B',
        'primary-element':'#99B898',
        'secondary-element':'#E84A5F',
        'third-element':'#FF847C',
        'fourth-element': '#FECEAB'
      },
    },
  },
  plugins: [],
});
