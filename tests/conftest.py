import os
import sys
from pathlib import Path

import pytest
from werkzeug.security import generate_password_hash

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app as flask_app
from db import get_db, init_db
from selenium import webdriver

def _ensure_ingredient(db, name):
    row = db.execute("SELECT id FROM ingredients WHERE name = ?", (name,)).fetchone()
    if row is not None:
        return row["id"]

    cursor = db.execute("INSERT INTO ingredients (name) VALUES (?)", (name,))
    return cursor.lastrowid


def _create_recipe(db, *, title, description, instructions, user_id, ingredients):
    cursor = db.execute(
        """
        INSERT INTO recipes (title, description, instructions, user_id, difficulty, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, description, instructions, user_id, "easy", "published"),
    )
    recipe_id = cursor.lastrowid

    for ingredient in ingredients:
        ingredient_id = _ensure_ingredient(db, ingredient)
        db.execute(
            """
            INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
            VALUES (?, ?)
            """,
            (recipe_id, ingredient_id),
        )

    return recipe_id


@pytest.fixture
def app(tmp_path):
    database_path = Path(tmp_path) / "test.sqlite"
    flask_app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
        DATABASE=database_path,
        WTF_CSRF_ENABLED=False,
    )

    with flask_app.app_context():
        init_db()
        db = get_db()

        db.execute(
            """
            INSERT INTO users (username, email, password_hash, bio, location)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                "Test Chef",
                "chef@example.com",
                generate_password_hash("password123", method="pbkdf2:sha256"),
                "Lives on pantry staples.",
                "Perth",
            ),
        )
        db.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (
                "Community Cook",
                "community@example.com",
                generate_password_hash("password123", method="pbkdf2:sha256"),
            ),
        )

        _create_recipe(
            db,
            title="pantry rice bowl",
            description="Quick rice bowl from pantry basics.",
            instructions="Cook rice.\nFry egg.\nMix with soy sauce.",
            user_id=None,
            ingredients=["egg", "rice", "soy sauce"],
        )
        _create_recipe(
            db,
            title="tomato egg rice",
            description="One more ingredient and dinner is sorted.",
            instructions="Cook rice.\nScramble egg.\nAdd tomato and serve.",
            user_id=None,
            ingredients=["egg", "rice", "tomato"],
        )
        _create_recipe(
            db,
            title="tuna mayo rice",
            description="A student classic.",
            instructions="Cook rice.\nMix tuna and mayo.\nServe together.",
            user_id=2,
            ingredients=["rice", "tuna", "mayo"],
        )

        db.commit()

    yield flask_app


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client



@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()