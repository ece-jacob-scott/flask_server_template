const plugin = require("tailwindcss/plugin");

module.exports = {
  content: [
    "./{{PROJECT_NAME}}/templates/**/*.html.*",
    "./{{PROJECT_NAME}}/templates/**/*.html",
    "./{{PROJECT_NAME}}/templates/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    plugin(function ({ addVariant }) {
      addVariant("htmx-settling", ["&.htmx-settling", ".htmx-settling &"]);
      addVariant("htmx-request", ["&.htmx-request", ".htmx-request &"]);
      addVariant("htmx-swapping", ["&.htmx-swapping", ".htmx-swapping &"]);
      addVariant("htmx-added", ["&.htmx-added", ".htmx-added &"]);
    }),
  ],
};
