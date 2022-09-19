from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
  return render_template("home.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signin")
def signin():
  return render_template("signin.html")

@app.route("/signup")
def signup():
  return render_template("signup.html")