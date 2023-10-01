from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from constellation_archives.models.system import System
from constellation_archives.models.planet import Planet

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
            "faction": request.form["controlling_faction"],
            "description": request.form["description"],
            "submitter": current_user.username
        }
        try:
            system = System(name=data["name"])
            flash("System already exists.")
            return redirect(url_for("locations.system", system=system.name))
        except:
            pass
        system = System.new(**data)
        flash("System created successfully.")
        return redirect(url_for("locations.system", system=system.name))
    
@app.route("/new/planet/", methods=["GET", "POST"])
def new_planet():
    if request.method == "GET":
        return render_template("locations/new_planet.html", page="new_planet")
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
            "resources": request.form["resources"],
            "traits": request.form["traits"],
            "moons": request.form["moons"],
            "description": request.form["description"],
            "submitter": current_user.username
        }
        try:
            planet = Planet(name=data["name"], system=data["system"])
            flash("Planet already exists.")
            return redirect(url_for("locations.planet", system=planet.system, planet=planet.name))
        except:
            pass
        planet = Planet.new(**data)
        flash("Planet created successfully.")
        return redirect(url_for("locations.planet", system=planet.system, planet=planet.name))