from flask import Blueprint, render_template, request, redirect, url_for, flash
from constellation_archives.models.settings import IndexSettings
from flask_login import current_user, login_required
from constellation_archives.models.user import User


app = Blueprint("admin", __name__)

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        if not current_user.has_role("admin"):
            flash("You do not have permission to view this page.", "error")
            return redirect(url_for("index"))
        data = {
            "settings": IndexSettings(id=1),
            "page": "admin_index",
        }
        return render_template("admin/index.html", **data)
    elif request.method == "POST":
        if not current_user.has_role("admin"):
            flash("You do not have permission to view this page.", "error")
            return redirect(url_for("index"))
        settings = IndexSettings(id=1)
        settings["main_text"] = request.form["main_text"]
        banner_enabled = request.form.get("banner_enabled", False)
        if banner_enabled:
            settings.enable_banner(request.form["banner_type"], request.form["banner_text"])
        else:
            settings.disable_banner()
        flash("Index settings updated.", "success")
        return redirect(url_for("admin.index"))

@app.route("/users/")
@login_required
def users():
    if not current_user.has_role("admin"):
        flash("You do not have permission to view this page.", "error")
        return redirect(url_for("index"))
    users = User.all()
    data = {
        "page": "admin_users",
        "users": users,
    }
    return render_template("admin/users.html", **data)

@app.route("/users/edit/<user_id>/", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if not current_user.has_role("admin"):
        flash("You do not have permission to view this page.", "error")
        return redirect(url_for("index"))
    user = User(id=user_id)
    if user != current_user:
        if user.has_role("admin") and not current_user.has_role("superadmin"):
            flash("You do not have permission to edit this user.", "danger")
            return redirect(url_for("admin.users"))
    if request.method == "GET":
        data = {
            "page": "admin_users",
            "user": user,
        }
        return render_template("admin/edit_user.html", **data)
    elif request.method == "POST":
        new_roles = request.form.getlist("roles")
        if "admin" in new_roles and not current_user.has_role("superadmin"):
            flash("You do not have permission to grant admin role.", "danger")
            return redirect(url_for("admin.users"))
        if "superadmin" in new_roles and not current_user.has_role("superadmin"):
            flash("You do not have permission to grant superadmin role.", "danger")
            return redirect(url_for("admin.users"))
        if user == current_user and "admin" not in new_roles:
            flash("You cannot remove your own admin role.", "danger")
            return redirect(url_for("admin.users"))
        if "roles" in request.form:
            user['roles'] = new_roles

        flash("User updated.", "success")
        return redirect(url_for("admin.users"))

@app.route("/users/delete/<user_id>/", methods=["GET"])
@login_required
def delete_user(user_id):
    if not current_user.has_role("admin"):
        flash("You do not have permission to view this page.", "error")
        return redirect(url_for("index"))
    try:
        user = User(id=user_id)
    except:
        flash("User '%s' not found." % user_id, "error")
        return redirect(url_for("admin.users"))
    user.delete()
    flash("User deleted.", "success")
    return redirect(url_for("admin.users"))