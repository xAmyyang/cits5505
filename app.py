from flask import Flask, render_template

app = Flask(__name__)


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
    return render_template("community.html")


@app.route("/saved")
def saved_recipes():
    return render_template("SavedRecipe.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/recipe")
def recipe_detail():
    return render_template("recipe-detail.html")


if __name__ == "__main__":
    app.run(debug=True)
