import json
from pathlib import Path

from flask import Flask, abort, render_template

app = Flask(__name__)
DATA_FILE = Path(__file__).parent / "data" / "recipes.json"


def load_recipes():
    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def get_recipe(recipe_id):
    recipes = load_recipes()
    return next((recipe for recipe in recipes if recipe["id"] == recipe_id), None)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/ingredients")
def ingredient_selection():
    return render_template("ingredient-selection.html")


@app.route("/community")
def community():
    recipes = load_recipes()
    return render_template("community.html", recipes=recipes)


@app.route("/saved")
def saved_recipes():
    return render_template("SavedRecipe.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


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
