BASE_URL = "http://127.0.0.1:5000"


def test_home_page(driver):
    driver.get(BASE_URL)
    assert driver.current_url == f"{BASE_URL}/"


def test_login_page(driver):
    driver.get(f"{BASE_URL}/login")
    assert "/login" in driver.current_url


def test_signup_page(driver):
    driver.get(f"{BASE_URL}/signup")
    assert "/signup" in driver.current_url


def test_ingredients_page(driver):
    driver.get(f"{BASE_URL}/ingredients")
    assert "/ingredients" in driver.current_url


def test_community_page(driver):
    driver.get(f"{BASE_URL}/community")
    assert "/community" in driver.current_url


def test_recipe_page(driver):
    driver.get(f"{BASE_URL}/recipe")
    assert "/recipe" in driver.current_url