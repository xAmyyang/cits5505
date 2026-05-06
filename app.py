import json
import os
import re
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db
from db import init_app as init_db_app

app = Flask(__name__)
DATA_FILE = Path(__file__).parent / "data" / "recipes.json"
app.config["SECRET_KEY"] = "dev"
database_override = os.environ.get("SURVIVECHEF_DATABASE")
if database_override:
    app.config["DATABASE"] = Path(database_override)
else:
    app.config["DATABASE"] = Path(app.instance_path) / "survivechef.db"
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
init_db_app(app)


def load_recipes():
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def get_recipe(recipe_id):
    recipes = load_recipes()
    return next((recipe for recipe in recipes if recipe["id"] == recipe_id), None)


def normalize_ingredients(raw_ingredients):
    cleaned = []
    for ingredient in raw_ingredients:
        value = ingredient.strip().lower()
        if value and value not in cleaned:
            cleaned.append(value)
    return cleaned


def categorize_recipes(selected_ingredients):
    selected_set = set(selected_ingredients)
    exact_matches = []
    one_away_matches = []

    for recipe in load_recipes():
        recipe_ingredients = set(recipe["ingredients"])
        missing_ingredients = sorted(recipe_ingredients - selected_set)

        if not missing_ingredients:
            exact_matches.append(recipe)
        elif len(missing_ingredients) == 1:
            recipe_with_gap = dict(recipe)
            recipe_with_gap["missing_ingredient"] = missing_ingredients[0]
            one_away_matches.append(recipe_with_gap)

    return exact_matches, one_away_matches


def get_saved_recipe_ids(user_id):
    db = get_db()
    rows = db.execute(
        "SELECT recipe_id FROM saved_recipes WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    return {row["recipe_id"] for row in rows}


def get_saved_recipes_for_user(user_id):
    saved_ids = []
    db = get_db()
    rows = db.execute(
        "SELECT recipe_id FROM saved_recipes WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    saved_ids = [row["recipe_id"] for row in rows]

    recipes_by_id = {recipe["id"]: recipe for recipe in load_recipes()}
    return [recipes_by_id[recipe_id] for recipe_id in saved_ids if recipe_id in recipes_by_id]


def annotate_saved_status(recipes, saved_ids):
    annotated = []
    for recipe in recipes:
        recipe_copy = dict(recipe)
        recipe_copy["is_saved"] = recipe["id"] in saved_ids
        annotated.append(recipe_copy)
    return annotated


def validate_email(email):
    return re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email) is not None


def find_user_by_email(email):
    db = get_db()
    return db.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,),
    ).fetchone()


def require_login():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return None


@app.context_processor
def inject_auth_state():
    return {
        "current_user_name": session.get("user_name"),
        "current_user_email": session.get("user_email"),
        "is_logged_in": bool(session.get("user_id")),
    }


@app.route("/")
def home():
    return render_template(
        "index.html",
        is_logged_in=session.get("user_id") is not None,
        current_user_name=session.get("user_name")
    )


@app.route("/login", methods=("GET", "POST"))
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    error = None
    form_data = {"email": ""}

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))
        form_data["email"] = email

        if not email or not password:
            error = "please enter both email and password"
        else:
            user = find_user_by_email(email)
            if user is None or not check_password_hash(user["password_hash"], password):
                error = "invalid email or password"
            else:
                session.clear()
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["user_email"] = user["email"]
                session.permanent = remember
                return redirect(url_for("profile"))

    return render_template("login.html", error=error, form_data=form_data)


@app.route("/signup", methods=("GET", "POST"))
def signup():
    if session.get("user_id"):
        return redirect(url_for("profile"))

    error = None
    form_data = {"name": "", "email": "", "terms": False}

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        accepted_terms = bool(request.form.get("terms"))

        form_data = {"name": name, "email": email, "terms": accepted_terms}

        if len(name) < 2:
            error = "name must be at least 2 characters"
        elif not validate_email(email):
            error = "please enter a valid email address"
        elif len(password) < 8:
            error = "password must be at least 8 characters"
        elif password != confirm:
            error = "passwords do not match"
        elif not accepted_terms:
            error = "please agree to the terms to continue"
        elif find_user_by_email(email) is not None:
            error = "an account with this email already exists"
        else:
            db = get_db()
            db.execute(
                """
                INSERT INTO users (name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (name, email, generate_password_hash(password)),
            )
            db.commit()

            user = find_user_by_email(email)
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            session.permanent = True
            return redirect(url_for("profile"))

    return render_template("signup.html", error=error, form_data=form_data)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/ingredients", methods=("GET", "POST"))
def ingredient_selection():
    if request.method == "POST":
        selected_ingredients = normalize_ingredients(
            request.form.getlist("ingredients")
        )
        if selected_ingredients:
            return redirect(
                url_for(
                    "recipe_results",
                    ingredients=",".join(selected_ingredients),
                )
            )

    return render_template("ingredient-selection.html")


@app.route("/results")
def recipe_results():
    selected_ingredients = normalize_ingredients(
        request.args.get("ingredients", "").split(",")
    )
    exact_matches, one_away_matches = categorize_recipes(selected_ingredients)
    saved_ids = get_saved_recipe_ids(session["user_id"]) if session.get("user_id") else set()

    return render_template(
        "recipe-results.html",
        selected_ingredients=selected_ingredients,
        exact_matches=annotate_saved_status(exact_matches, saved_ids),
        one_away_matches=annotate_saved_status(one_away_matches, saved_ids),
    )


@app.route("/community")
def community():
    recipes = load_recipes()
    return render_template("community.html", recipes=recipes)


@app.route("/saved")
def saved_recipes():
    redirect_response = require_login()
    if redirect_response is not None:
        return redirect_response

    recipes = get_saved_recipes_for_user(session["user_id"])
    return render_template("SavedRecipe.html", saved_recipes=recipes)


@app.route("/profile")
def profile():
    redirect_response = require_login()
    if redirect_response is not None:
        return redirect_response

    return render_template(
        "profile.html",
        user_name=session.get("user_name", "chef"),
        user_email=session.get("user_email", ""),
    )


@app.route("/recipe")
@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id=None):
    recipes = load_recipes()

    if not recipes:
        abort(404)

    if recipe_id is None:
        recipe = recipes[0]
    else:
        recipe = get_recipe(recipe_id)
        if recipe is None:
            abort(404)

    saved_ids = get_saved_recipe_ids(session["user_id"]) if session.get("user_id") else set()
    recipe_data = dict(recipe)
    recipe_data["is_saved"] = recipe["id"] in saved_ids

    return render_template("recipe-detail.html", recipe=recipe_data)


@app.route("/save/<int:recipe_id>", methods=("POST",))
def save_recipe(recipe_id):
    redirect_response = require_login()
    if redirect_response is not None:
        return redirect_response

    if get_recipe(recipe_id) is None:
        abort(404)

    db = get_db()
    db.execute(
        """
        INSERT OR IGNORE INTO saved_recipes (user_id, recipe_id)
        VALUES (?, ?)
        """,
        (session["user_id"], recipe_id),
    )
    db.commit()

    return redirect(request.form.get("next") or url_for("saved_recipes"))


@app.route("/unsave/<int:recipe_id>", methods=("POST",))
def unsave_recipe(recipe_id):
    redirect_response = require_login()
    if redirect_response is not None:
        return redirect_response

    db = get_db()
    db.execute(
        "DELETE FROM saved_recipes WHERE user_id = ? AND recipe_id = ?",
        (session["user_id"], recipe_id),
    )
    db.commit()

    return redirect(request.form.get("next") or url_for("saved_recipes"))


if __name__ == "__main__":
    app.run(debug=True)
