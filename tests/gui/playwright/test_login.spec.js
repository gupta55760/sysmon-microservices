const { test, expect } = require('@playwright/test');
const { LoginPage } = require('./pages/login_page');
const { loadTestData } = require('../../../utils/dataLoader');

const loginData = require('../../data/login_data_gui');
//const loginData = loadTestData('login_data_gui.csv');

for (const { username, password, should_pass } of loginData) {
  test(`Login Test - username: "${username || '(empty)'}", password: "${password || '(empty)'}"`, async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(username, password);

    if (should_pass) {
      // ✅ Successful login → dashboard heading should appear
      await expect(page.locator('h1')).toHaveText(/SysMon Dashboard/i);
    } else {
      if (username && password) {
        // ❌ Wrong credentials → JS alert expected
        const [dialog] = await Promise.all([
          page.waitForEvent('dialog'),
          loginPage.login(username, password) // triggers the alert
        ]);
        expect(dialog.message()).toContain('Login error');
        await dialog.accept();
      } else {
        // ❌ Empty input → login blocked, still on login page
        await expect(page).toHaveURL('http://localhost:3000');
      }
    }
  });
}

