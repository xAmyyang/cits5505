# Test if the home page loads successfully
def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


# Test if the login page loads successfully
def test_login_page(client):
    response = client.get("/login")

    assert response.status_code == 200


# Test if the signup page loads successfully
def test_signup_page(client):
    response = client.get("/signup")

    assert response.status_code == 200


# Test if the ingredient selection page loads successfully
def test_ingredients_page(client):
    response = client.get("/ingredients")

    assert response.status_code == 200