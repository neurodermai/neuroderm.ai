/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        // Peaceful color palette
        sage: {
          50: '#f6f7f6',
          100: '#e3e7e3',
          200: '#c7d0c7',
          300: '#a3b1a3',
          400: '#7d8f7d',
          500: '#5f725f',
          600: '#4a5b4a',
          700: '#3d4a3d',
          800: '#333d33',
          900: '#2c332c',
        },
        sky: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
        lavender: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7c3aed',
          800: '#6b21a8',
          900: '#581c87',
        },
        sand: {
          50: '#fdfcfb',
          100: '#faf6f1',
          200: '#f5ede0',
          300: '#ede0c8',
          400: '#e2ccaa',
          500: '#d4b58c',
          600: '#c49a6c',
          700: '#a87d52',
          800: '#8a6644',
          900: '#715439',
        },
        // Base colors
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "#5f725f",
          foreground: "#ffffff",
        },
        secondary: {
          DEFAULT: "#f6f7f6",
          foreground: "#333d33",
        },
        muted: {
          DEFAULT: "#f6f7f6",
          foreground: "#7d8f7d",
        },
        accent: {
          DEFAULT: "#e3e7e3",
          foreground: "#3d4a3d",
        },
      },
      borderRadius: {
        lg: "1rem",
        md: "0.75rem",
        sm: "0.5rem",
        xl: "1.5rem",
        "2xl": "2rem",
        "3xl": "3rem",
      },
      fontFamily: {
        sans: ['var(--font-nunito)', 'system-ui', 'sans-serif'],
        display: ['var(--font-playfair)', 'serif'],
      },
      keyframes: {
        "float": {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        "breathe": {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.8' },
          '50%': { transform: 'scale(1.05)', opacity: '1' },
        },
        "wave": {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        "fadeIn": {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        "pulse-soft": {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
      animation: {
        "float": "float 6s ease-in-out infinite",
        "breathe": "breathe 4s ease-in-out infinite",
        "wave": "wave 8s ease-in-out infinite",
        "fadeIn": "fadeIn 0.6s ease-out",
        "pulse-soft": "pulse-soft 3s ease-in-out infinite",
      },
      backgroundImage: {
        'gradient-peaceful': 'linear-gradient(135deg, #f6f7f6 0%, #e3e7e3 50%, #f0f9ff 100%)',
        'gradient-sunset': 'linear-gradient(135deg, #faf5ff 0%, #f3e8ff 50%, #faf6f1 100%)',
        'gradient-ocean': 'linear-gradient(180deg, #e0f2fe 0%, #bae6fd 50%, #f0f9ff 100%)',
        'gradient-forest': 'linear-gradient(135deg, #e3e7e3 0%, #c7d0c7 50%, #a3b1a3 100%)',
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}