import random
import string
from flask import Flask, render_template, redirect, request
import json

app = Flask(__name__)
shortened_urls = {}


def generate_short_urls(length=6):
    chars = string.ascii_letters + string.digits
    short_urls = " ".join(random.choice(chars) for _ in range(length))
    return short_urls


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_urls = generate_short_urls()
        while short_urls in shortened_urls:
            short_urls = generate_short_urls()

        shortened_urls[short_urls] = long_url
        # with open("urls.json", "w" as  f):
        #     json.dump(shortened_urls, f)

        return f"Shortened URL {request.url_root}{short_urls}"
    return render_template("index.html")


@app.route("/<short_urls>")
def redirect_url(short_urls):
    long_url = shortened_urls.get(short_urls)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404



if __name__ == "__main__":
    app.run(debug=True)
