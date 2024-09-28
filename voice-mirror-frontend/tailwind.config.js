/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,tsx,ts,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#F5F5F5", // Light Neutral Gray for a minimal background
        secondary: "#FFFFFF", // Crisp White for contrast
        primaryText: "#2C3E50", // Dark Blue-Gray for professional readability
        secondaryText: "#7F8C8D", // Soft Gray for secondary text
        linkText: "#2980B9", // Refined Deep Blue for links
        primaryButton: "#34495E", // Dark Blue-Gray for a sophisticated, solid primary button
        secondaryButton: "#BDC3C7", // Light Cool Gray for secondary button
        primaryButtonHover: "#2C3E50", // Slightly darker shade on hover
        primaryBorder: "#DADFE1", // Light Gray for subtle borders
        success: "#27AE60", // Calm Green for success states
        error: "#C0392B", // Mature Deep Red for errors
        warning: "#E67E22", // Muted Warm Orange for warnings, not too bold
        inputBackground: "#FFFFFF", // Clean White for input fields
        inputBorder: "#DADFE1", // Same as primary border for consistency
        inputFocus: "#2980B9", // Subtle blue to highlight focus state
        formLabelText: "#7F8C8D", // Soft Gray for form labels
        primaryButtonText: "#FFFFFF", // White for strong contrast on dark buttons
        secondaryButtonText: "#2C3E50", // Dark Blue-Gray for text on light buttons
      },
    },
  },
  plugins: [],
};
