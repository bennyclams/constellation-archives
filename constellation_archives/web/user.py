from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from constellation_archives.models.user import User

app = Blueprint("users", __name__)

@app.route("/profile/")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            user = User(username=username)
        except:
            user = None

        if user is None:
            flash("Invalid username or password", "error")
        elif not user.check_password(password):
            flash("Invalid username or password", "error")
        else:
            flash("Logged in successfully", "success")
            login_user(user)
            return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("index"))

@app.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        try:
            user = User(username=username)
        except:
            user = None

        if user is None:
            try:
                user = User(email=email)
            except:
                user = None

        if user is not None:
            flash("Username or email already exists", "error")
        else:
            user = User.new(username=username, email=email, password=password, roles=["user"])
            flash("Registered successfully", "success")
            return redirect(url_for("users.login"))

    return render_template("register.html")