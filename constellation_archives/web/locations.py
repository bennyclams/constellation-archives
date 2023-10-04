from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from constellation_archives.models.system import System
from constellation_archives.models.planet import Planet
from constellation_archives.web.utils import upload_file_to_s3

app = Blueprint("locations", __name__)

@app.route("/systems/")
def systems():
    data = {
        "systems": System.all(),
        "page": "systems"
    }
    return render_template("locations/systems.html", **data)

@app.route("/s/<system>/")
def system(system):
    data = {
        "system": System(name=system),
        "planets": Planet.by_system(system),
        # "planets": [],
        "page": "systems"
    }
    return render_template("locations/system.html", **data)

@app.route("/s/<system>/<planet>/")
def planet(system, planet):
    data = {
        "system": System(name=system),
        "planet": Planet(name=planet),
        "page": "systems"
    }
    return render_template("locations/planet.html", **data)

@app.route("/new/system/", methods=["GET", "POST"])
def new_system():
    if request.method == "GET":
        return render_template("locations/new_system.html", page="new_system")
    elif request.method == "POST":
        banner = request.files["banner"]
        if banner.filename != "":
            banner = upload_file_to_s3(banner)
        else:
            banner = banner.filename

        data = {
            "name": request.form["name"],
            "level": request.form["level"],
            "class": request.form["class"],
            "catalogue_id": request.form["catalogue"],
            "temperature": request.form["temperature"],
            "mass": request.form["mass"],
            "radius": request.form["radius"],
            "magnitude": request.form["magnitude"],
            "planet_count": request.form["planets"],
            "moon_count": request.form["moons"],
            "faction": request.form["faction"],
            "description": request.form["description"],
            "banner": banner,
            "submitter": current_user['username']
        }
        try:
            system = System(name=data["name"])
            flash("System already exists.", "warning")
            return redirect(url_for("locations.system", system=system['name']))
        except:
            pass
        system = System.new(**data)
        flash("System created successfully.", "success")
        return redirect(url_for("locations.system", system=system['name']))
    
@app.route("/new/planet/", methods=["GET", "POST"])
def new_planet():
    if request.method == "GET":
        data = {
            "systems": System.all(),
            "page": "new_planet"
        }
        return render_template("locations/new_planet.html", **data)
    elif request.method == "POST":
        data = {
            "name": request.form["name"],
            "system": request.form["system"],
            "type": request.form["type"],
            "gravity": request.form["gravity"],
            "temperature": request.form["temperature"],
            "atmosphere": request.form["atmosphere"],
            "magnetosphere": request.form["magnetosphere"],
            "fauna": request.form["fauna"],
            "flora": request.form["flora"],
            "water": request.form["water"],
            "resources": request.form.getlist("resources"),
            "traits": request.form.getlist("traits"),
            "moons": request.form.getlist("moons"),
            "description": "",
            "submitter": current_user['username']
        }
        try:
            planet = Planet(name=data["name"], system=data["system"])
            flash("Planet already exists.", "warning")
            return redirect(url_for("locations.planet", system=planet['system'], planet=planet['name']))
        except:
            pass
        planet = Planet.new(**data)
        flash("Planet created successfully.", "success")
        return redirect(url_for("locations.planet", system=planet['system'], planet=planet['name']))
    
@app.route("/edit/system/<system_name>/", methods=["GET", "POST"])
def edit_system(system_name):
    if request.method == "GET":
        try:
            system = System(name=system_name)
        except:
            flash("System '%s' does not exist." % system_name, "warning")
            return redirect(url_for("locations.systems"))
        data = {
            "system": system,
            "page": "edit_system"
        }
        return render_template("locations/edit_system.html", **data)
    elif request.method == "POST":
        system_name = request.form["name"]
        try:
            system = System(name=system_name)
        except:
            flash("System '%s' does not exist." % system_name, "warning")
            return redirect(url_for("locations.systems"))
        data = {}
        for field in request.form:
            if field == "submitter":
                continue
            if field in system:
                if request.form[field] != system[field]:
                    data[field] = request.form[field]
        if request.files["banner"].filename != "":
            data["banner"] = upload_file_to_s3(request.files["banner"])
        system.update(**data)
        print(data)
        flash("System updated successfully.", "success")
        return redirect(url_for("locations.system", system=system['name']))