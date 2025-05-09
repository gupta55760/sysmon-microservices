# login_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators Section (TOP of class)
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Username"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Password"]')
    LOGIN_BUTTON = (By.TAG_NAME, "button")
    DASHBOARD_HEADING = (By.TAG_NAME, "h1")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_login(self):
        self.navigate_to("http://localhost:3000")

    def login(self, username, password):
        self.type(*self.USERNAME_INPUT, username)
        self.type(*self.PASSWORD_INPUT, password)
        self.click(*self.LOGIN_BUTTON)

    def get_dashboard_heading(self):
        return self.get_text(*self.DASHBOARD_HEADING)

    def is_login_successful(self):
        try:
            self.wait_for_visible(*self.DASHBOARD_HEADING, timeout=5)
            return True
        except:
            return False
