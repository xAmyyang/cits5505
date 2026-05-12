import os
import re
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db
from db import init_app as init_db_app

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"
database_override = os.environ.get("SURVIVECHEF_DATABASE")
if database_override:
    app.config["DATABASE"] = Path(database_override)
else:
    app.config["DATABASE"] = Path(app.instance_path) / "survivechef.db"
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
init_db_app(app)


def load_recipes():
    db = get_db()

    recipe_rows = db.execute(
        """
        SELECT
            recipes.id,
            recipes.title,
            recipes.description,
            recipes.instructions,
            recipes.user_id,
            recipes.created_at,
            users.username AS author_name
        FROM recipes
        LEFT JOIN users ON users.id = recipes.user_id
        ORDER BY id
        """
    ).fetchall()

    recipes = []

    for row in recipe_rows:
        ingredient_rows = db.execute(
            """
            SELECT i.name
            FROM ingredients i
            JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
            WHERE ri.recipe_id = ?
            ORDER BY i.name
            """,
            (row["id"],),
        ).fetchall()

        recipes.append({
            "id": row["id"],
            "name": row["title"],
            "title": row["title"],
            "description": row["description"],
            "instructions": row["instructions"],
            "steps": normalize_steps((row["instructions"] or "").splitlines()) or [row["instructions"] or ""],
            "ingredients": [ingredient["name"] for ingredient in ingredient_rows],
            "time": "10 min",
            "difficulty": "easy",
            "user_id": row["user_id"],
            "author_name": row["author_name"] or "SurviveChef",
        })

    return recipes


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


def normalize_steps(raw_steps):
    return [step.strip() for step in raw_steps if step.strip()]


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


def get_all_ingredients():
    db = get_db()
    rows = db.execute(
        """
        SELECT name
        FROM ingredients
        ORDER BY name
        """
    ).fetchall()
    return [row["name"] for row in rows]


def load_shared_recipes():
    return [recipe for recipe in load_recipes() if recipe["user_id"] is not None]


def get_or_create_ingredient_ids(ingredient_names):
    db = get_db()
    ingredient_ids = []

    for ingredient in ingredient_names:
        row = db.execute(
            "SELECT id FROM ingredients WHERE name = ?",
            (ingredient,),
        ).fetchone()

        if row is None:
            cursor = db.execute(
                "INSERT INTO ingredients (name) VALUES (?)",
                (ingredient,),
            )
            ingredient_ids.append(cursor.lastrowid)
        else:
            ingredient_ids.append(row["id"])

    return ingredient_ids


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
    db = get_db()

    recipe_count = db.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
    user_count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    ingredient_count = db.execute("SELECT COUNT(*) FROM ingredients").fetchone()[0]

    return render_template(
        "index.html",
        is_logged_in=session.get("user_id") is not None,
        current_user_name=session.get("user_name"),
        recipe_count=recipe_count,
        user_count=user_count,
        ingredient_count=ingredient_count
    )

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
                session["user_name"] = user["username"]
                session["user_email"] = user["email"]
                session.permanent = remember
                return redirect(url_for("home"))

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
                INSERT INTO users (username, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (name, email, generate_password_hash(password)),
            )
            db.commit()

            user = find_user_by_email(email)
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["username"]
            session["user_email"] = user["email"]
            session.permanent = True
            return redirect(url_for("profile"))

    return render_template("signup.html", error=error, form_data=form_data)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


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

    return render_template(
        "ingredient-selection.html",
        available_ingredients=get_all_ingredients(),
    )


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
    return render_template("community.html", recipes=load_shared_recipes())


@app.route("/recipes/new", methods=("GET", "POST"))
def new_recipe():
    redirect_response = require_login()
    if redirect_response is not None:
        return redirect_response

    error = None
    form_data = {
        "name": "",
        "ingredients": "",
        "steps": "",
        "description": "",
        "difficulty": "easy",
    }

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        ingredients = normalize_ingredients(request.form.get("ingredients", "").split(","))
        steps = normalize_steps(request.form.get("steps", "").splitlines())
        description = request.form.get("description", "").strip()
        difficulty = request.form.get("difficulty", "easy").strip().lower()
        form_data = {
            "name": name,
            "ingredients": request.form.get("ingredients", ""),
            "steps": request.form.get("steps", ""),
            "description": description,
            "difficulty": difficulty,
        }

        if len(name) < 3:
            error = "recipe name must be at least 3 characters"
        elif len(ingredients) < 2:
            error = "please add at least 2 ingredients"
        elif len(steps) < 2:
            error = "please add at least 2 cooking steps"
        elif difficulty not in {"easy", "medium", "hard"}:
            error = "please choose a valid difficulty"
        else:
            db = get_db()
            instructions = "\n".join(steps)
            description_value = description or "Shared by the community."
            cursor = db.execute(
                """
                INSERT INTO recipes (title, description, instructions, user_id)
                VALUES (?, ?, ?, ?)
                """,
                (name, description_value, instructions, session["user_id"]),
            )
            recipe_id = cursor.lastrowid

            for ingredient_id in get_or_create_ingredient_ids(ingredients):
                db.execute(
                    """
                    INSERT INTO recipe_ingredients (recipe_id, ingredient_id)
                    VALUES (?, ?)
                    """,
                    (recipe_id, ingredient_id),
                )

            db.commit()
            return redirect(url_for("community"))

    return render_template("share-recipe.html", error=error, form_data=form_data)


@app.route("/saved")
def saved_recipes():
    redirect_response = require_login()
    if redirect_response is not None:
        return redirect_response

    recipes = get_saved_recipes_for_user(session["user_id"])
    return render_template("SavedRecipe.html", saved_recipes=recipes)


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()

    # 1. user
    user = db.execute(
        "SELECT id, username, email, bio, location, avatar_url FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()
    # 2. stats — 
    stats = db.execute("""
        SELECT
            (SELECT COUNT(*)
             FROM recipes WHERE user_id = ?)          AS recipe_count,
            (SELECT COUNT(*)
             FROM saved_recipes WHERE user_id = ?)    AS saved_count,
            (SELECT COALESCE(SUM(likes), 0)
             FROM recipes WHERE user_id = ?)          AS total_likes
    """, (session["user_id"],) * 3).fetchone()
    # 3. recipes — ingredient_count 
    recipes = db.execute("""
        SELECT r.id, r.title, r.emoji, r.difficulty,
               r.likes, r.status,
               COUNT(ri.ingredient_id) AS ingredient_count
        FROM   recipes r
        LEFT JOIN recipe_ingredients ri ON ri.recipe_id = r.id
        WHERE  r.user_id = ?
        GROUP  BY r.id
        ORDER  BY r.created_at DESC
    """, (session["user_id"],)).fetchall()
    # 4. achievements
    achievements = db.execute("""
        SELECT a.icon, a.title, a.desc,
               (ua.user_id IS NOT NULL) AS unlocked
        FROM       achievements a
        LEFT JOIN  user_achievements ua
               ON  ua.achievement_id = a.id
               AND ua.user_id = ?
        ORDER BY   a.sort_order
    """, (session["user_id"],)).fetchall()
    return render_template("profile.html",
        user=user,
        stats=stats,
        recipes=recipes,
        achievements = achievements,
    )
@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        bio = request.form.get("bio", "").strip()
        location = request.form.get("location", "").strip()
        avatar_url = request.form.get("avatar_url", "").strip()

        db.execute(
            """
            UPDATE users
            SET username = ?, bio = ?, location = ?, avatar_url = ?
            WHERE id = ?
            """,
            (username, bio, location, avatar_url, session["user_id"])
        )
        db.commit()

        return redirect(url_for("profile"))

    user = db.execute(
        "SELECT id, username, email, bio, location, avatar_url FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    return render_template("edit_profile.html", user=user)

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
