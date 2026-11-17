
from flask import Flask, render_template, redirect, url_for, request
import requests
from datetime import datetime
from database import create_database, save_joke, get_jokes, delete_joke

app = Flask(__name__)

create_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_joke")
def get_joke():
    category = request.args.get("category", "Any")

    allowed_categories = [
        "Any", "Programming", "Misc",
        "Dark", "Pun", "Spooky", "Christmas"
    ]

    if category not in allowed_categories:
        category = "Any"

    url = f"https://v2.jokeapi.dev/joke/{category}?safe-mode"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            return "Joke not found"

        if data["type"] == "single":
            joke_text = data["joke"]
        else:
            joke_text = data["setup"] + "\n\n" + data["delivery"]

        save_joke(
            data["category"],
            joke_text,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        return render_template(
            "index.html",
            joke=joke_text,
            category=data["category"]
        )

    except requests.RequestException:
        return "API connection error"


@app.route("/history")
def history():
    jokes = get_jokes()
    return render_template("index.html", jokes=jokes)


@app.route("/delete/<int:joke_id>")
def delete(joke_id):
    delete_joke(joke_id)
    return redirect(url_for("history"))


if __name__ == "__main__":
    app.run(debug=True)
