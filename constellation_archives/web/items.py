from flask import Blueprint, render_template, request, redirect, url_for, flash
from constellation_archives.web.utils import upload_file_to_s3
from constellation_archives.models.item_type import ItemType
from constellation_archives.models.category import Category
from constellation_archives.models.item import Item
from flask_login import current_user
import markdown2


app = Blueprint("items", __name__)

@app.route("/categories/")
def categories_index():
    categories = Category.all()
    data = {
        "categories": categories,
        "page": "categories",
    }
    return render_template("categories.html", **data)

@app.route("/types/")
def types_index():
    types = ItemType.all()
    data = {
        "types": types,
        "page": "types",
    }
    return render_template("types.html", **data)

@app.route("/c/<category_name>/")
def category(category_name):
    category = Category(name=category_name)
    items = Item.by_category(category_name)
    data = {
        "category": category,
        "items": items,
        "page": "categories",
    }
    return render_template("category.html", **data)

@app.route("/t/<item_type>/")
def item_type(item_type):
    item_type = ItemType(name=item_type)
    items = Item.by_type(item_type)
    data = {
        "items": items,
        "item_type": item_type,
        "page": "types",
    }
    return render_template("type.html", **data)

@app.route("/i/<item_id>/")
def item(item_id):
    item = Item(id=item_id)
    item._data['description'] = markdown2.markdown(item['description'])
    data = {
        "item": item,
        "page": "item",
    }
    return render_template("item.html", **data)

@app.route("/new/type/", methods=["GET", "POST"])
def new_type():
    if request.method == "GET":
        if current_user.has_role("creation_restricted"):
            flash("You do not have permission to create a new item type", "error")
            return redirect(url_for("index"))
        return render_template("new_type.html", page="new_type")
    elif request.method == "POST":
        if current_user.has_role("creation_restricted"):
            flash("You do not have permission to create a new item type", "error")
            return redirect(url_for("index"))
        name = request.form["name"]
        if ItemType.exists(name=name):
            flash("Item type already exists", "error")
            return redirect(url_for("new_type"))
        ItemType.new(name=name, submitter=current_user['username'])
        flash("Item type created", "success")
        return redirect(url_for("types_index"))
    
@app.route("/new/category/", methods=["GET", "POST"])
def new_category():
    if request.method == "GET":
        if current_user.has_role("creation_restricted"):
            flash("You do not have permission to create a new category", "error")
            return redirect(url_for("index"))
        return render_template("new_category.html", page="new_category")
    elif request.method == "POST":
        if current_user.has_role("creation_restricted"):
            flash("You do not have permission to create a new category", "error")
            return redirect(url_for("index"))
        name = request.form["name"]
        description = request.form["description"]
        thumbnail = request.files["thumbnail"]
        if thumbnail.filename != "":
            thumbnail_filename = upload_file_to_s3(thumbnail)
        else:
            thumbnail_filename = "no-thumb.png"
        if Category.exists(name=name):
            flash("Category already exists", "error")
            return redirect(url_for("new_category"))
        Category.new(name=name, description=description, thumbnail=thumbnail_filename, submitter=current_user['username'])
        flash("Category created", "success")
        return redirect(url_for("categories_index"))
    
@app.route("/new/item/", methods=["GET", "POST"])
def new_item():
    if request.method == "GET":
        if current_user.has_role("creation_restricted"):
            flash("You do not have permission to create a new item", "error")
            return redirect(url_for("index"))
        categories = Category.all()
        types = ItemType.all()
        data = {
            "categories": categories,
            "types": types,
            "page": "new_item",
        }
        return render_template("new_item.html", **data)
    elif request.method == "POST":
        if current_user.has_role("creation_restricted"):
            flash("You do not have permission to create a new item", "error")
            return redirect(url_for("index"))
        name = request.form["name"]
        item_type = request.form["type"]
        description = request.form["description"]
        images = request.files.getlist("images")
        image_paths = []
        for image in images:
            if image.filename != "":
                image_filename = upload_file_to_s3(image)
            else:
                image_filename = "no-image.png"
            image_paths.append(image_filename)
        # images = []
        categories = request.form.getlist("categories")
        item = Item.new(name=name, item_type=item_type, description=description, images=image_paths, categories=categories, submitter=current_user['username'])
        flash("Item created", "success")
        return redirect(url_for("item", item_id=item['id']))