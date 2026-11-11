from flask import Blueprint, request, jsonify, abort
from ..helpers.utils import generate_db_conn

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
