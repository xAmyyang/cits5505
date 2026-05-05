import json
import re
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db
from db import init_app as init_db_app

app = Flask(__name__)
DATA_FILE = Path(__file__).parent / "data" / "recipes.json"
app.config["SECRET_KEY"] = "dev"
app.config["DATABASE"] = Path(app.instance_path) / "survivechef.db"
Path(app.instance_path).mkdir(parents=True, exist_ok=True)
init_db_app(app)


def load_recipes():
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def get_recipe(recipe_id):
    recipes = load_recipes()
    return next((recipe for recipe in recipes if recipe["id"] == recipe_id), None)


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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=("GET", "POST"))
def login():
    if session.get("user_id"):
        return redirect(url_for("home"))

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
        return redirect(url_for("home"))

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


@app.route("/ingredients")
def ingredient_selection():
    return render_template("ingredient-selection.html")


@app.route("/community")
def community():
    recipes = load_recipes()
    return render_template("community.html", recipes=recipes)


@app.route("/saved")
def saved_recipes():
    redirect_response = require_login()
    if redirect_response is not None:
        return redirect_response
    return render_template("SavedRecipe.html")


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

    return render_template("recipe-detail.html", recipe=recipe)


if __name__ == "__main__":
    app.run(debug=True)
