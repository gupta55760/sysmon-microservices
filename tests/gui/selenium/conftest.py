# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import sys
import os

THIS_DIR = os.path.dirname(__file__)
if THIS_DIR not in sys.path:
    sys.path.insert(0, THIS_DIR)


# Add custom CLI options
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use: chrome or firefox")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")

# Fixture to create WebDriver based on CLI options
@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--window-size=1280,800")
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1280")
        options.add_argument("--height=800")
        driver = webdriver.Firefox(options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield driver
    driver.quit()

# Create folder for screenshots under tests/reports/selenium/screenshots
def ensure_screenshot_dir():
    tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    screenshots_dir = os.path.join(tests_dir, "reports", "selenium", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)
    return screenshots_dir

# Hook to capture screenshot on failure + attach to HTML report
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshots_dir = ensure_screenshot_dir()
            filename = os.path.join(screenshots_dir, f"{item.name}.png")
            driver.save_screenshot(filename)
            print(f"\n📸 Screenshot saved: {filename}")

            # Attach to pytest-html report (if enabled)
            if hasattr(report, "extra"):
                from pytest_html import extras
                rel_path = os.path.relpath(filename, start=os.getcwd())
                report.extra.append(extras.image(rel_path))

