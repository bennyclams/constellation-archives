from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from constellation_archives.web.utils import upload_file_to_s3
from constellation_archives.models.item_type import ItemType
from constellation_archives.models.category import Category
from constellation_archives.web.user import app as user_app
from constellation_archives.web.items import app as items_app
from constellation_archives.web.locations import app as locations_app
from constellation_archives.models.item import Item
from constellation_archives.models.user import User
from flask_login import LoginManager, current_user
from flask_session import Session
import markdown2
import redis
import os


app = Flask(__name__, template_folder="../templates")
app.register_blueprint(user_app, url_prefix="/users")
app.register_blueprint(items_app)
app.register_blueprint(locations_app)
login_manager = LoginManager()
redis_db = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
app.config["REDIS_DB"] = redis_db
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", os.urandom(32))
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_REDIS"] = redis_db
Session(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User(id=int(user_id))

@app.route("/")
def index():
    return render_template("index.html", page="home")

