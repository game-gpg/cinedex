# Cinedex

A small movie and TV catalog built with Python and Flask. It has a poster grid, search, genre filter, sorting, and a detail page for each title with links to legal places to watch it and a trailer search.

## Run it

```
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Structure

- `app.py` - routes (home with search/filter/sort, movie detail, 404)
- `data.py` - sample catalog and the list of streaming services
- `templates/` - Jinja pages
- `static/style.css` - dark responsive theme

## Next steps

- Replace `data.py` with a call to the TMDB API (free key) for real posters and a full catalog.
- Add pagination, a TV series type, and a watchlist.
