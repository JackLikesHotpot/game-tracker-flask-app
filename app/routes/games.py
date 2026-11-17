from flask import Blueprint, request, jsonify, abort
from ..helpers.utils import generate_db_conn
from ..services.igdb import igdb_post
from..services.populate_db import convert_game_to_row, push_to_db
import arrow

games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.get('/catalogue')
def get_all_games():
    """
    Queries database for all games and returns them.
    """
    conn = generate_db_conn()
    try:
        rows = conn.execute('SELECT * FROM games ORDER BY title').fetchall()
    finally:
        conn.close()

    if not rows:
        abort(404, description='Game database not found!')
    
    return jsonify(rows), 200


@games_bp.get('/catalogue/<game_id>')
def get_game_by_id(game_id):
    """
    Queries database for one game of a given ID and returns it.
    """
    conn = generate_db_conn()
    try:
        game = conn.execute(f'SELECT * FROM games WHERE game_id={game_id}').fetchone()
    finally:
        conn.close()

    if not game:
        abort(404, description=f'Game of ID {game_id} not found!')

    return jsonify(game), 200

@games_bp.get('/catalogue/<genre>')
def get_games_by_genre(genre):
    """
    Queries database for all games of a given genre and returns it.
    """
    conn = generate_db_conn()
    try:
        games = conn.execute(f'SELECT * FROM games where genre ILIKE %{genre}%').fetchall()
    finally:
        conn.close()

    if not games:
        abort(404, description='Game database not found!')

    return jsonify(games), 200

@games_bp.get('/catalogue/search')
def search():
    """
    Queries database via game name and genre from query parameters in URL, and returns a result.
    """
    game_name = request.args.get(key='name', default='')
    conn = generate_db_conn()
    try:
        games = conn.execute(f"SELECT * FROM games where title ILIKE '%{game_name}%'").fetchall()
    finally:
        conn.close()
    
    if not games:
        abort(404, description=f'Game of title {game_name} not found!')

    return jsonify(games), 200


@games_bp.post('/catalogue')
def add_game():
    # check credentials before adding
    """
    POST request which requires JSON body containing the title (and optionally the release year) of a game to be queried in the IGDB API before being added to the database.
    """
    data = request.get_json(silent=True)
    title = data.get('title', '')
    release_year = data.get('year')

    if not data:
        return jsonify({"error": "JSON body containing title and year is required for POST request"}), 400
    if not title:
        return jsonify({"error": "Title is required in JSON body"}), 400

    where = ""
    if release_year:
        start, end = arrow.get(release_year, 1, 1).span('year')
        where = f"where first_release_date >= {start.int_timestamp} & first_release_date < {end.int_timestamp}"
    query = f"""
    search "{title}";
    fields id, name, summary, first_release_date, genres.name, cover.url; 
    {where};
    limit 10;
    """
    try:
        games = igdb_post('games', query=query)
        if not games:
            abort(404, description=f"No game called '{title}' found on IGDB")        
        game_tuple = convert_game_to_row(games[0])
        push_to_db(game_tuple, 'single')
        return jsonify({"message": "Added game successfully!"}), 201
    except Exception as e:
        raise
