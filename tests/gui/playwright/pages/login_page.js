// tests/gui/pages/login_page.js

class LoginPage {
  constructor(page) {
    this.page = page;
    this.usernameInput = page.locator('input[placeholder="Username"]');
    this.passwordInput = page.locator('input[placeholder="Password"]');
    this.loginButton = page.locator('button');
  }

  async goto() {
    await this.page.goto('http://localhost:3000');
  }

  async login(username, password) {
    if (username !== undefined) await this.usernameInput.fill(username);
    if (password !== undefined) await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}

module.exports = { LoginPage };

