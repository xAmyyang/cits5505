import socket
import threading
from contextlib import closing

import pytest
from werkzeug.serving import make_server

selenium = pytest.importorskip("selenium")

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("127.0.0.1", 0))
        sock.listen(1)
        return sock.getsockname()[1]


def _wait_for_text(driver, text):
    WebDriverWait(driver, 10).until(
        lambda current_driver: text.lower() in current_driver.page_source.lower()
    )


def _login(driver, base_url):
    driver.get(f"{base_url}/login")
    driver.find_element(By.ID, "loginEmail").send_keys("chef@example.com")
    driver.find_element(By.ID, "loginPassword").send_keys("password123")
    driver.find_element(By.ID, "loginSubmitBtn").click()
    WebDriverWait(driver, 10).until(EC.url_to_be(f"{base_url}/"))


@pytest.fixture
def live_server(app):
    port = _free_port()
    server = make_server("127.0.0.1", port, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture
def browser():
    try:
        driver = webdriver.Safari()
    except WebDriverException as exc:
        pytest.skip(f"Safari WebDriver unavailable: {exc}")

    driver.implicitly_wait(2)
    yield driver
    driver.quit()


@pytest.mark.selenium
def test_signup_flow(browser, live_server):
    browser.get(f"{live_server}/signup")
    browser.find_element(By.ID, "signupName").send_keys("Browser Student")
    browser.find_element(By.ID, "signupEmail").send_keys("browser@example.com")
    browser.find_element(By.ID, "signupPassword").send_keys("password123")
    browser.find_element(By.ID, "signupConfirm").send_keys("password123")
    browser.find_element(By.ID, "agreeTerms").click()
    browser.find_element(By.ID, "signupSubmitBtn").click()

    WebDriverWait(browser, 10).until(EC.url_contains("/profile"))
    _wait_for_text(browser, "browser@example.com")


@pytest.mark.selenium
def test_login_flow(browser, live_server):
    _login(browser, live_server)
    _wait_for_text(browser, "log out")


@pytest.mark.selenium
def test_ingredient_selection_flow(browser, live_server):
    browser.get(f"{live_server}/ingredients")
    browser.find_element(By.CSS_SELECTOR, '[data-ingredient="egg"]').click()
    browser.find_element(By.CSS_SELECTOR, '[data-ingredient="rice"]').click()
    browser.find_element(By.CSS_SELECTOR, '[data-ingredient="soy sauce"]').click()
    browser.find_element(By.ID, "findRecipesBtn").click()

    WebDriverWait(browser, 10).until(EC.url_contains("/results"))
    _wait_for_text(browser, "pantry rice bowl")


@pytest.mark.selenium
def test_share_recipe_flow(browser, live_server):
    _login(browser, live_server)
    browser.get(f"{live_server}/recipes/new")
    browser.find_element(By.ID, "recipeName").send_keys("browser chilli eggs")
    browser.find_element(By.ID, "recipeDescription").send_keys("Fast browser coverage.")
    browser.find_element(By.ID, "recipeIngredients").send_keys("egg, chilli oil, rice")
    browser.find_element(By.ID, "recipeSteps").send_keys("Cook rice.\nFry egg.\nTop with chilli oil.")
    browser.find_element(By.ID, "recipeDifficulty").send_keys("Easy")
    browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    WebDriverWait(browser, 10).until(EC.url_contains("/community"))
    _wait_for_text(browser, "browser chilli eggs")


@pytest.mark.selenium
def test_save_recipe_flow(browser, live_server):
    _login(browser, live_server)
    browser.get(f"{live_server}/results?ingredients=egg,rice,soy sauce")
    browser.find_element(By.CSS_SELECTOR, ".results-save-btn").click()
    browser.get(f"{live_server}/saved")

    _wait_for_text(browser, "pantry rice bowl")
