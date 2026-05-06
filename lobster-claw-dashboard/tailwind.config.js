/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ocean: '#071018',
        brass: '#cf9c42',
        claw: '#dc3b34',
        tube: '#2ad8ca',
      },
    },
  },
  plugins: [],
};
