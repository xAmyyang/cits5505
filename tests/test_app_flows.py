from db import get_db


def test_signup_creates_account_and_redirects_to_profile(client, app):
    response = client.post(
        "/signup",
        data={
            "name": "New Student",
            "email": "new@example.com",
            "password": "password123",
            "confirm": "password123",
            "terms": "on",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/profile")

    with app.app_context():
        user = get_db().execute(
            "SELECT username, email FROM users WHERE email = ?",
            ("new@example.com",),
        ).fetchone()

    assert user["username"] == "New Student"


def test_signup_rejects_duplicate_email(client):
    response = client.post(
        "/signup",
        data={
            "name": "Copy Cat",
            "email": "chef@example.com",
            "password": "password123",
            "confirm": "password123",
            "terms": "on",
        },
    )

    assert response.status_code == 200
    assert b"an account with this email already exists" in response.data


def test_login_sets_session_and_redirects_home(client):
    response = client.post(
        "/login",
        data={"email": "chef@example.com", "password": "password123"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    with client.session_transaction() as session:
        assert session["user_name"] == "Test Chef"
        assert session["user_email"] == "chef@example.com"


def test_save_recipe_requires_login(client):
    response = client.post("/save/1", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")


def test_ingredient_selection_redirects_to_results(client):
    response = client.post(
        "/ingredients",
        data={"ingredients": ["egg", "rice", "soy sauce"]},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/results?ingredients=egg,rice,soy+sauce")


def test_results_show_exact_and_one_away_matches(client):
    response = client.get("/results?ingredients=egg,rice")

    assert response.status_code == 200
    assert b"Pantry Rice Bowl" in response.data
    assert b"Tomato Egg Rice" in response.data
    assert b"Missing: <strong>soy sauce</strong>" in response.data
    assert b"Missing: <strong>tomato</strong>" in response.data


def test_new_recipe_creates_recipe_and_ingredients(client, app):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_name"] = "Test Chef"
        session["user_email"] = "chef@example.com"

    response = client.post(
        "/recipes/new",
        data={
            "name": "late night noodles",
            "description": "Fast and cheap.",
            "ingredients": "noodles, egg, chilli oil",
            "steps": "Boil noodles.\nFry egg.\nMix and serve.",
            "difficulty": "easy",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/community")

    with app.app_context():
        db = get_db()
        recipe = db.execute(
            "SELECT id, title, user_id FROM recipes WHERE title = ?",
            ("late night noodles",),
        ).fetchone()
        ingredients = db.execute(
            """
            SELECT i.name
            FROM ingredients i
            JOIN recipe_ingredients ri ON ri.ingredient_id = i.id
            WHERE ri.recipe_id = ?
            ORDER BY i.name
            """,
            (recipe["id"],),
        ).fetchall()

    assert recipe["user_id"] == 1
    assert [row["name"] for row in ingredients] == ["chilli oil", "egg", "noodles"]


def test_save_recipe_persists_for_logged_in_user(client, app):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_name"] = "Test Chef"
        session["user_email"] = "chef@example.com"

    response = client.post(
        "/save/1",
        data={"next": "/saved"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/saved")

    with app.app_context():
        saved = get_db().execute(
            "SELECT recipe_id FROM saved_recipes WHERE user_id = ?",
            (1,),
        ).fetchall()

    assert [row["recipe_id"] for row in saved] == [1]


def test_unsave_missing_recipe_returns_404_for_logged_in_user(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_name"] = "Test Chef"
        session["user_email"] = "chef@example.com"

    response = client.post("/unsave/999", follow_redirects=False)

    assert response.status_code == 404


def test_edit_profile_updates_session_name(client, app):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_name"] = "Test Chef"
        session["user_email"] = "chef@example.com"

    response = client.post(
        "/profile/edit",
        data={
            "username": "Night Cook",
            "bio": "Still surviving.",
            "location": "Perth",
            "avatar_url": "https://example.com/avatar.png",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/profile")

    with client.session_transaction() as session:
        assert session["user_name"] == "Night Cook"

    with app.app_context():
        user = get_db().execute(
            "SELECT username, bio, avatar_url FROM users WHERE id = ?",
            (1,),
        ).fetchone()

    assert user["username"] == "Night Cook"
    assert user["bio"] == "Still surviving."
    assert user["avatar_url"] == "https://example.com/avatar.png"


def test_edit_profile_rejects_short_username(client):
    with client.session_transaction() as session:
        session["user_id"] = 1
        session["user_name"] = "Test Chef"
        session["user_email"] = "chef@example.com"

    response = client.post(
        "/profile/edit",
        data={
            "username": "A",
            "bio": "Short name attempt.",
            "location": "Perth",
            "avatar_url": "",
        },
        follow_redirects=False,
    )

    assert response.status_code == 200
    assert b"username must be at least 2 characters" in response.data
