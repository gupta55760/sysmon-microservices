# pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def navigate_to(self, url):
        print(f"➡️ Navigating to {url}")
        self.driver.get(url)

    def find(self, by, value):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((by, value))
            )
            print(f"🔍 Found element by {by}: {value}")
            return element
        except TimeoutException:
            print(f"❌ Timeout finding element by {by}: {value}")
            raise

    def click(self, by, value, retries=2):
        for attempt in range(retries):
            try:
                element = self.find(by, value)
                self.scroll_into_view(element)
                element.click()
                print(f"🖱️ Clicked element by {by}: {value}")
                return
            except ElementClickInterceptedException:
                print(f"⚠️ Click intercepted! Retrying ({attempt+1})...")
                time.sleep(1)
        raise Exception(f"❌ Failed to click after {retries} attempts: {by}, {value}")

    def type(self, by, value, text):
        element = self.find(by, value)
        element.clear()
        element.send_keys(text)
        print(f"⌨️ Typed into element {by}: {value} -> {text}")

    def get_text(self, by, value):
        element = self.find(by, value)
        text = element.text
        print(f"📄 Text from {by}: {value} -> {text}")
        return text

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def is_field_visible(self, locator):
        try:
            element = self.find(*locator)
            visible = element.is_displayed()
            print(f"👀 Visibility of {locator}: {visible}")
            return visible
        except:
            return False

    def wait_for_visible(self, by, value, timeout=None):
        actual_timeout = timeout if timeout else self.timeout
        try:
            WebDriverWait(self.driver, actual_timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            print(f"✅ Element visible: {by} {value}")
        except TimeoutException:
            print(f"❌ Timeout waiting for visibility: {by} {value}")
            raise

