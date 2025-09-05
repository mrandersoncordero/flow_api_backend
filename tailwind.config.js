/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./webapp/templates/**/*.html",
    "./static/src/**/*.js"
  ],
  theme: {
    darkMode: 'class',
    extend: {
      colors: {
        colors: {
          background: '#0a0a0a',
          foreground: '#fafafa',
          card: '#111111',
          'card-foreground': '#fafafa',
          primary: '#f97316',
          'primary-foreground': '#0a0a0a',
          secondary: '#1a1a1a',
          'secondary-foreground': '#fafafa',
          muted: '#262626',
          'muted-foreground': '#a3a3a3',
          accent: '#f97316',
          'accent-foreground': '#0a0a0a',
          border: '#262626',
          input: '#1a1a1a',
          ring: '#f97316'
        }
      }
    },
  },
  plugins: [],
}
