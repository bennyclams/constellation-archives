from flask import Flask, render_template, redirect, url_for, flash, session
from constellation_archives.web.locations import app as locations_app
from constellation_archives.models.settings import IndexSettings
from constellation_archives.models.latest_adds import LatestAdds
from constellation_archives.web.items import app as items_app
from constellation_archives.web.admin import app as admin_app
from constellation_archives.web.user import app as user_app
from constellation_archives.models.user import User
from datetime import datetime, timedelta
from flask_login import LoginManager
from flask_session import Session
import markupsafe
import markdown2
import bleach
import redis
import os


app = Flask(__name__, template_folder="../templates")
app.register_blueprint(user_app, url_prefix="/users")
app.register_blueprint(items_app)
app.register_blueprint(locations_app)
app.register_blueprint(admin_app, url_prefix="/admin")
login_manager = LoginManager()
redis_db = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
app.config["REDIS_DB"] = redis_db
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", os.urandom(32))
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis_db
app.config["STATIC_URL"] = os.getenv("STATIC_URL", "/static")
Session(app)
login_manager.init_app(app)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)

@app.context_processor
def inject_template():
    return dict(static_url=app.config["STATIC_URL"])

@app.template_filter("markdown")
def markdown_filter(s):
    bleached = bleach.clean(s, tags=bleach.ALLOWED_TAGS + [
        "p", 
        "h1", 
        "h2", 
        "h3", 
        "h4", 
        "h5",
        "h6", 
        "blockquote", 
        "pre", 
        "code", 
        "em", 
        "strong", 
        "ul", 
        "ol", 
        "li", 
        "a", 
        "img", 
        "br", 
        "hr", 
        "div", 
        "span", 
        "table", 
        "thead", 
        "tbody", 
        "tr", 
        "th", 
        "td", 
        "caption"
    ], attributes=bleach.ALLOWED_ATTRIBUTES)
    return markupsafe.Markup(markdown2.markdown(bleached))

@login_manager.user_loader
def load_user(user_id):
    return User(id=int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view this page.", "warning")
    return redirect(url_for("users.login"))

@app.route("/")
def index():
    items = []
    for item in LatestAdds().all():
        item["created_at"] = datetime.fromisoformat(item["created_at"])
        item["updated_at"] = datetime.fromisoformat(item["updated_at"])
        items.append(item)
    items.reverse()
    data = {
        "settings": IndexSettings(id=1),
        "latest": items,
        "page": "home",
    }
    return render_template("index.html", **data)

