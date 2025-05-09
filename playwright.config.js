// playwright.config.js (at project root)
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  timeout: 30000,
  retries: 0,
  testDir: 'tests/gui/playwright',
  use: {
    headless: false,  // 👈 run in headed mode
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  reporter: [
  ['list'],  // ✅ terminal output with ✓ ✘
  ['html', { outputFolder: 'tests/reports/playwright', open: 'never' }]
],
});


