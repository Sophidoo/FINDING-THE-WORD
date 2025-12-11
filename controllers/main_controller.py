from flask import render_template
from flask_login import login_required

def base():
    return render_template("base.html")

def contact():
    return render_template("contact.html")

@login_required
def game():
    return render_template("game.html")

def index():
    return render_template("index.html")

@login_required
def leaderboard():
    return render_template("leaderboard.html")

def login():
    return render_template("login.html")

@login_required
def profile():
    return render_template("profile.html")

def register():
    return render_template("register.html")
