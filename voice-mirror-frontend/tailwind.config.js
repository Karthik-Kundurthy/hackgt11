/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,tsx,ts,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#E0F7FA",
        secondary: "#FFFFFF",
        primaryText: "#000000",
        secondaryText: "#474F4F",
        linkText: "#1565C0",
        primaryButton: "#1565C0",
        secondaryButton: "#4FC3F7",
        primaryButtonHover: "#0288D1",
        primaryBorder: "#B0BEC5",
        success: "#43A047",
        error: "#E53935",
        warning: "#FB8C00",
        inputBackground: "#FFFFFF",
        inputBorder: "#B0BEC5",
        inputFocus: "#0288D1",
        formLabelText: "#4F4F4F",
        primaryButtonText: "#FFFFFF",
        secondaryButtonText: "#000000",
      },
    },
  },
  plugins: [],
};
