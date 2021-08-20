import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_catalogue")
def get_catalogue():
    catalogue = mongo.db.catalogue.find()
    return render_template("catalogue.html", catalogue=catalogue)


# User Authentication adapted from 'Task Manager' mini-project by CI
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successful")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


# User Authentication adapted from 'Task Manager' mini-project by CI
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    reviews = mongo.db.reviews.find()

    if session["user"]:
        return render_template(
            "profile.html", username=username, reviews=reviews)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        review = {
            "username": session["user"],
            "game_title": request.form.get("game_title"),
            "review_text": request.form.get("review_text"),
            "date_created": datetime.now(),
            "game_rating": request.form.get("game_rating")
        }
        mongo.db.reviews.insert_one(review)
        flash("Review Added")
        return redirect(url_for('profile', username=session['user']))

    titles = mongo.db.catalogue.find().sort("game_title", 1)
    return render_template("add_review.html", titles=titles)


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if request.method == "POST":
        submit = {
            "username": session["user"],
            "game_title": request.form.get("game_title"),
            "review_text": request.form.get("review_text"),
            "date_created": datetime.now(),
            "game_rating": request.form.get("game_rating")
        }
        mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
        flash("Review Successfully Updated")
        return redirect(url_for('profile', username=session['user']))

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

    titles = mongo.db.catalogue.find().sort("game_title", 1)
    return render_template("edit_review.html", review=review, titles=titles)


@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Task Successfully Deleted")
    return redirect(url_for('profile', username=session['user']))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
