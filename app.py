from flask import Flask, render_template

app = Flask(__name__)

# homepage
@app.route("/")
def home():
    return render_template("index.html")


# 如果你有其他页面，比如 login / about，可以这样加
@app.route("/login")
def login():
    return render_template("login.html")




# 启动服务器
if __name__ == "__main__":
    app.run(debug=True)