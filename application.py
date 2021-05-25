from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request
from random import randint

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///imdb.db")


@app.route("/", methods=["GET", "POST"])
def index():
    """"Show main homepage where user selects from different categories"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # delete previous result entry inserted by index function
        db.execute("DELETE FROM result")

        # verify which type of genre was selected, if "Any" was selected assign % to genre variable
        genre = request.form.get("genre")
        if genre == "Any":
            genre = "%"

        # verify minimum rating selected, if "Any" was selected assign 0 to rating variable
        rating = request.form.get("rating")
        if rating == "Any":
            rating = 0
        # verify minimum year selected, if "Any" was selected assign 0 to year variable
        year = request.form.get("year")
        if year == "Any":
            year = 0

        # verify latest year selected, if "Any" was selected assign 0 to rating variable
        latest_year = request.form.get("latest_year")
        if latest_year == "Any":
            latest_year = 2021

        # verify which language was selected, if "Any" was selected assign % to language variable
        language = request.form.get("language")
        if language == "Any":
            language = "%"

        # main query, based on user provided data, concerning English speaking or any other language speaking movies
        if language != "Other":
            movies = db.execute("SELECT original_title, year, description, duration, avg_vote, country, imdb_title_id, genre FROM movies WHERE genre LIKE ? AND avg_vote >= ? AND year >= ? AND year < ? AND language LIKE ? AND votes >= 15000",
                                (f'%{genre}%'), rating, year, latest_year, (f'{language}%'))

        # main query, based on user provided data; if "other" was picked as language, query specifically for non-English languages
        else:
            movies = db.execute("SELECT original_title, year, description, duration, avg_vote, country, imdb_title_id, genre FROM movies WHERE genre LIKE ? AND avg_vote >= ? AND year >= ? AND year < ? AND language NOT LIKE ? AND votes >= 15000",
                                (f'%{genre}%'), rating, year, latest_year, 'English%')

        # find out length of the queried list stored in movies and substract 1 in order to set the end number for the randomizer
        last_row = len(movies) - 1

        # continue if at least one result is found
        if last_row >= 0:

            # pick a random number between 0 and the last row of movies
            random_number = randint(0, last_row)

            # store selected movie name via the movies list's randomly-selected row
            db.execute("INSERT INTO result (original_title, year, description, duration, avg_vote, country, imdb_title_id, genre) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       movies[random_number]["original_title"], movies[random_number]["year"], movies[random_number]["description"], movies[random_number]["duration"], movies[random_number]["avg_vote"], movies[random_number]["country"], movies[random_number]["imdb_title_id"], movies[random_number]["genre"])

            # redirect to another function once result is stored
            return redirect("/result")

        # create a new apology template if no results are found
        else:
            return render_template("apology.html", genre=genre, year=year, latest_year=latest_year)

    # User reached route via GET (as by clicking a link or via a redirect)
    else:
        return render_template("index.html")


@app.route("/result")
def result():
    """Show the movie selected by the randomizer"""

    # query for the movie picked by the randomizer
    result = db.execute("SELECT * FROM result")

    # render a new template with the result
    return render_template("result.html", result=result)

