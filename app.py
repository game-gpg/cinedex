from urllib.parse import quote_plus

from flask import Flask, abort, render_template, request

from data import MOVIES, PROVIDERS

app = Flask(__name__)

ALL_GENRES = sorted({g for m in MOVIES for g in m["genres"]})
SORTS = {
    "rating": ("Top rated", lambda m: -m["rating"]),
    "newest": ("Newest", lambda m: -m["year"]),
    "oldest": ("Oldest", lambda m: m["year"]),
    "title": ("A to Z", lambda m: m["title"].lower()),
}


@app.template_filter("hue")
def hue(movie_id):
    """Deterministic colour for the placeholder poster."""
    return (movie_id * 47) % 360


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    genre = request.args.get("genre", "")
    sort = request.args.get("sort", "rating")
    if sort not in SORTS:
        sort = "rating"

    results = MOVIES
    if q:
        ql = q.lower()
        results = [
            m for m in results
            if ql in m["title"].lower()
            or ql in m["director"].lower()
            or any(ql in c.lower() for c in m["cast"])
        ]
    if genre in ALL_GENRES:
        results = [m for m in results if genre in m["genres"]]
    results = sorted(results, key=SORTS[sort][1])

    return render_template(
        "index.html", movies=results, q=q, genre=genre, sort=sort,
        genres=ALL_GENRES, sorts={k: v[0] for k, v in SORTS.items()},
    )


@app.route("/movie/<int:movie_id>")
def movie(movie_id):
    m = next((x for x in MOVIES if x["id"] == movie_id), None)
    if m is None:
        abort(404)
    q = quote_plus(m["title"])
    providers = [(name, url.format(q=q)) for name, url in PROVIDERS.items()]
    trailer = f"https://www.youtube.com/results?search_query={q}+{m['year']}+official+trailer"
    similar = [
        x for x in MOVIES
        if x["id"] != m["id"] and set(x["genres"]) & set(m["genres"])
    ][:4]
    return render_template("movie.html", m=m, providers=providers, trailer=trailer, similar=similar)


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
