import pytest
import sys
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.data_loader import load_test_data


def as_bool(value):
    if isinstance(value, bool):
        return value
    return value.strip().lower() == "true"

def get_login_test_data():
    # Choose source: CSV or JSON
    data = load_test_data("login_data_gui.csv")
    #data = load_test_data("login_data_gui.json")
    print(f"test_data is {data}")
    return [
        (row["username"], row["password"], as_bool(row["should_pass"]))
        for row in data
    ]

@pytest.mark.parametrize("username,password,should_pass", get_login_test_data())
def test_login_variants(driver, username, password, should_pass):
    login_page = LoginPage(driver)
    login_page.navigate_to_login()
    login_page.login(username, password)

    if should_pass:
        try:
            h1_text = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(login_page.DASHBOARD_HEADING)
            ).text
            assert "SysMon Dashboard" in h1_text
        except TimeoutException:
            driver.save_screenshot(f"screenshots/test_login_success_dashboard_not_found_{username}.png")
            pytest.fail("❌ Dashboard did not load — possible login failure.")
    else:
        if username and password:
            try:
                WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                assert "Login error" in alert.text
                alert.accept()
            except TimeoutException:
                driver.save_screenshot(f"screenshots/test_login_failure_alert_not_found_{username}.png")
                pytest.fail("❌ Expected alert popup not found for wrong credentials.")
        else:
            current_url = driver.current_url
            if "localhost:3000" not in current_url:
                driver.save_screenshot(f"screenshots/test_login_empty_submission_failed_{username}.png")
                pytest.fail("❌ Form submitted despite empty fields!")

