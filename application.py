import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///chiza.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show your books"""
    active_user = session["user_id"]

    books_info = db.execute("SELECT * FROM books WHERE id = (SELECT book_id FROM library WHERE user_id = ?)", active_user)

    library = db.execute("SELECT * FROM library WHERE user_id = ?", active_user)

    if request.method == "POST":

        pages_read = request.form.get("page")

        book_id = request.form.get("id")

        db.execute("UPDATE library SET pages_read = ? WHERE user_id = ? AND book_id = ?", pages_read, active_user, book_id)

        finished_books = db.execute("SELECT * FROM library WHERE user_id = ? AND book_id = ?", active_user, book_id)

        all_books = db.execute("SELECT * FROM books")

        total_books = len(all_books)

        users_books = len(library)

        for book in finished_books:
            if book["pages"] == book["pages_read"]:
                db.execute("UPDATE library SET read = ? WHERE user_id = ? AND book_id = ?", 1, active_user, book["book_id"])

                finished = db.execute("SELECT * FROM library WHERE read = ? AND user_id = ?", 1, active_user)

                books_finished = len(finished)

                if total_books != books_finished:
                    return render_template("finished.html", total_books=total_books, books_finished=books_finished)

                return render_template("final.html")

        return redirect("/")

    else:

        for book in books_info:
            for book2 in library:
                if book2["book_id"] == book["id"]:
                    book2["pages"] = book["pages"]

        books = []

        reads = []

        for row in library:

            line = {}

            line["id"] = row["book_id"]
            line["pages_read"] = row["pages_read"]
            line["pages"] = row["pages"]
            line["pages_read"] = row["pages_read"]
            line["percent"] = round((row["pages_read"] * 100) / row["pages"])

            if row["read"] == 1:
                reads.append(line)

            else:

                books.append(line)


        return render_template("index.html", books=books, reads=reads)


@app.route("/collection", methods=["GET", "POST"])
@login_required
def collection():
    """Show book collection"""
    active_user = session["user_id"]

    if request.method == "POST":

        book_id = request.form.get("id")

        books = db.execute("SELECT * FROM books where id = ?", book_id)

        for book in books:
            book_pages = book["pages"]

        library = db.execute("SELECT * FROM library WHERE user_id = ? AND book_id = ?", active_user, book_id)

        if len(library) > 0:
            return apology("BOOK ALREADY ADDED")

        db.execute("INSERT INTO library (user_id, book_id, pages) VALUES (?, ?, ?)", active_user, book_id, book_pages)

        return redirect("/")

    else:

        books = db.execute("SELECT * FROM books")

        return render_template("collection.html", books=books)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        if not request.form.get("username") or not request.form.get("password"):
            return apology("COMPLETE THE REGISTRATION FORM")

        usernames = db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username"))

        if usernames:
            return apology("USERNAME ALREADY TAKEN")

        password = request.form.get("password")

        password_check = set()

        for letter in password:
            if letter.isupper():
                password_check.add(1)
            elif letter.isalpha():
                password_check.add(2)
            elif letter.isnumeric():
                password_check.add(3)
            else:
                password_check.add(4)

        print(len(password_check))

        if len(password_check) != 4:
            return apology("PASSWORD MUST CONTAIN NUMBERS, SYMBOLS, UPPER AND LOWER CASE LETTERS")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("PASSWORDS MUST MATCH")

        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)

        return redirect("/")

    else:

        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
