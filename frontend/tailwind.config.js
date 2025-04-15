module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Tells Tailwind to purge unused styles in production from all JS/TS files in src
  ],
  theme: {
    extend: {
      colors: {
        primary: '#FF6347', // Example custom color
        secondary: '#4CAF50', // Example custom color
      },
    },
  },
  plugins: [],
}
