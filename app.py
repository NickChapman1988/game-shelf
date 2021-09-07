import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_paginate import Pagination, get_page_args
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


def get_games(offset=0, per_page=10):
    catalogue = list(mongo.db.catalogue.find().sort("average_rating", -1))
    return catalogue[offset: offset + per_page]


@app.route("/")
@app.route("/home")
def home():
    latest_reviews = mongo.db.reviews.find().sort("date_created", -1).limit(4)

    return render_template("home.html", latest_reviews=latest_reviews)


@app.route("/get_catalogue")
def get_catalogue(offset=0, per_page=10):

    catalogue = list(mongo.db.catalogue.find().sort("average_rating", -1))
    latest_reviews = mongo.db.reviews.find().sort("date_created", -1).limit(4)

    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page')
    total = len(catalogue)
    pagination_games = get_games(offset=offset, per_page=per_page)
    pagination = Pagination(
        page=page, per_page=per_page, total=total)

    return render_template(
        "catalogue.html", catalogue=pagination_games,
        page=page, per_page=per_page, pagination=pagination,
        latest_reviews=latest_reviews)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    catalogue = list(mongo.db.catalogue.find({"$text": {"$search": query}}))
    latest_reviews = mongo.db.reviews.find().sort("date_created", -1).limit(4)

    return render_template(
        "search.html", catalogue=catalogue, latest_reviews=latest_reviews)


@app.route("/view_game/<game_id>")
def view_game(game_id):
    catalogue = mongo.db.catalogue.find()

    # find game in database
    game = mongo.db.catalogue.find_one({"_id": ObjectId(game_id)})
    # pull game title from database
    title = mongo.db.catalogue.find_one(game)["game_title"]
    # find reviews for game title, sort by most recent
    reviews = list(mongo.db.reviews.find(
        {"game_title": title}).sort("date_created", -1))

    # check if game already reviewed by user
    existing_review = mongo.db.reviews.find_one(
        {"game_title": title, "username": session['user']})

    return render_template(
        "view_game.html", game=game, catalogue=catalogue,
        reviews=reviews, existing_review=existing_review)

# ------------------------------------- User Authentication -----------


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

    reviews = mongo.db.reviews.find({
        "username": session["user"]}).sort("date_created", -1)

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

# ------------------ Review Functions ----------------------


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":

        # check if game already reviewed by user
        existing_review = mongo.db.reviews.find_one(
            {"game_title": request.form.get(
                "game_title"), "username": session['user']})

        if existing_review:
            flash("You've already reviewed this game!")
            return redirect(url_for('profile', username=session['user']))

        else:
            review = {
                "username": session["user"],
                "game_title": request.form.get("game_title"),
                "review_title": request.form.get("review_title"),
                "review_text": request.form.get("review_text"),
                "date_created": datetime.now(),
                "game_rating": request.form.get("game_rating")
            }

            # grab review game title
            game_title = request.form.get("game_title")

            mongo.db.reviews.insert_one(review)
            flash("Review Added")

            # grab updated reviews list for game
            reviews = list(mongo.db.reviews.find({"game_title": game_title}))

            # Calculate new average_rating and update db
            if len(reviews) == 0:
                average_rating = ""
            else:
                ratings = 0
                for review in reviews:
                    ratings = ratings + int(review.get("game_rating"))
                    average_rating = ratings / len(reviews)
                    mongo.db.catalogue.update({"game_title": game_title}, {
                        "$set": {"average_rating": average_rating}})

            return redirect(url_for('profile', username=session['user']))

    titles = mongo.db.catalogue.find().sort("game_title", 1)
    return render_template("add_review.html", titles=titles)


@app.route("/edit_review/<review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    if request.method == "POST":
        submit = {
            "username": session["user"],
            "game_title": request.form.get("game_title"),
            "review_title": request.form.get("review_title"),
            "review_text": request.form.get("review_text"),
            "date_created": datetime.now(),
            "game_rating": request.form.get("game_rating")
        }

        # grab review game title
        game_title = request.form.get("game_title")

        mongo.db.reviews.update({"_id": ObjectId(review_id)}, submit)
        flash("Review Successfully Updated")

        # grab updated reviews list for game
        reviews = list(mongo.db.reviews.find({"game_title": game_title}))
        # Calculate new average_rating and update db
        if len(reviews) == 0:
            average_rating = ""
        else:
            ratings = 0
            for review in reviews:
                ratings = ratings + int(review.get("game_rating"))
                average_rating = ratings / len(reviews)
                mongo.db.catalogue.update({"game_title": game_title}, {
                    "$set": {"average_rating": average_rating}})

        return redirect(url_for('profile', username=session['user']))

    review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})

    titles = mongo.db.catalogue.find().sort("game_title", 1)
    return render_template("edit_review.html", review=review, titles=titles)


@app.route("/delete_review/<review_id>")
def delete_review(review_id):
    mongo.db.reviews.remove({"_id": ObjectId(review_id)})
    flash("Task Successfully Deleted")
    return redirect(url_for('profile', username=session['user']))

# -------------------- Admin Game Functions ------------------


@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    if session["user"] == "admin":
        if request.method == "POST":

            # check if game already exists in db
            existing_game = mongo.db.catalogue.find_one(
                {"game_title": request.form.get("game_title")})

            if existing_game:
                flash("Game already added!")
                return redirect(url_for('profile', username=session['user']))

            else:

                game = {
                    "game_title": request.form.get("game_title"),
                    "game_description": request.form.get("game_description"),
                    "description_para_1": request.form.get(
                        "description_para_1"),
                    "description_para_2": request.form.get(
                        "description_para_2"),
                    "description_para_3": request.form.get(
                        "description_para_3"),
                    "description_para_4": request.form.get(
                        "description_para_4"),
                    "description_para_5": request.form.get(
                        "description_para_5"),
                    "min_player_count": request.form.get("min_player_count"),
                    "max_player_count": request.form.get("max_player_count"),
                    "min_play_time": request.form.get("min_play_time"),
                    "max_play_time": request.form.get("max_play_time"),
                    "min_player_age": request.form.get("min_player_age"),
                    "release_year": request.form.get("release_year"),
                    "designer": request.form.get("designer"),
                    "artist": request.form.get("artist"),
                    "publisher": request.form.get("publisher"),
                    "image_url": request.form.get("image_url"),
                    "shop_link": request.form.get("shop_link"),
                    "average_rating": 0
                }

                mongo.db.catalogue.insert_one(game)
                flash("Game Added Successfully")
                return redirect(url_for('profile', username=session['user']))

    else:
        flash("Sorry, you don't have permission to access this page")
        return redirect(url_for('get_catalogue'))

    titles = list(mongo.db.catalogue.find().sort("game_title", 1))
    return render_template("add_game.html", titles=titles)


@app.route("/edit_game/<game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    if request.method == "POST":
        submit = {
                "game_title": request.form.get("game_title"),
                "game_description": request.form.get("game_description"),
                "description_para_1": request.form.get("description_para_1"),
                "description_para_2": request.form.get("description_para_2"),
                "description_para_3": request.form.get("description_para_3"),
                "description_para_4": request.form.get("description_para_4"),
                "description_para_5": request.form.get("description_para_5"),
                "min_player_count": request.form.get("min_player_count"),
                "max_player_count": request.form.get("max_player_count"),
                "min_play_time": request.form.get("min_play_time"),
                "max_play_time": request.form.get("max_play_time"),
                "min_player_age": request.form.get("min_player_age"),
                "release_year": request.form.get("release_year"),
                "designer": request.form.get("designer"),
                "artist": request.form.get("artist"),
                "publisher": request.form.get("publisher"),
                "image_url": request.form.get("image_url"),
                "shop_link": request.form.get("shop_link"),
                # prevent average_rating resetting
                "average_rating": mongo.db.catalogue.find_one(
                    {"game_title": request.form.get(
                        "game_title")})["average_rating"]
            }

        mongo.db.catalogue.update({"_id": ObjectId(game_id)}, submit)
        flash("Game Updated Successfully")
        return redirect(url_for('get_catalogue'))

    game = mongo.db.catalogue.find_one({"_id": ObjectId(game_id)})

    titles = list(mongo.db.catalogue.find().sort("game_title", 1))
    return render_template("edit_game.html", game=game, titles=titles)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
