import arrow
import psycopg
import os
import requests
import logging
from dotenv import load_dotenv
from .igdb import igdb_post

load_dotenv()
logger = logging.getLogger(__name__)

def get_games_by_date(limit=500):
    """
    Get a list a maximum of 500 games between 2 dates and return it.
    """
    start_date = arrow.get("2020-01-01").int_timestamp
    end_date = arrow.utcnow().floor("day").int_timestamp

    query = f"""
        fields id, name, summary, first_release_date, genres.name, cover.url; 
        where first_release_date >= {start_date} & first_release_date < {end_date}; 
        sort first_release_date asc; 
        limit {limit};
    """
    try:
        return igdb_post('games', query)
    except requests.Timeout:
        logger.error('IGDB request timed out, try again later.')
        raise
    except requests.HTTPError as e:
        status = e.response.status_code
        if status == 401:
            logger.error('Missing valid credentials, check Twitch access code/secret.')
        if status == 429:
            logger.error('Too many requests, try again later.')



def convert_game_to_row(game):
    """
    Used to convert games from list to tuples for SQL storage.
    """
    cover_image_url = None
    
    game_id = game['id']
    title = game['name']
    description = game.get('summary') or ''
    release_year = arrow.get(game['first_release_date']).year
    genres = game.get('genres') or []
    genre_names = ", ".join(g["name"] for g in genres) or None    
    cover = game.get('cover')
    if cover:
        cover_image_url = f"https:{cover['url']}"

    return (game_id, title, description, release_year, genre_names, cover_image_url)

import psycopg


def push_to_db(game_row):
    """
    Uses Psycopg to push the tuple of a game into the database, does nothing if there's a conflict.
    """
    conn = psycopg.connect(os.environ.get('DATABASE_URL'))
    try:
        cur = conn.cursor()
        cur.executemany(
            """INSERT INTO games (game_id, title, description, release_year, genre, cover_image_url)
               VALUES (%s, %s, %s, %s, %s, %s)
               ON CONFLICT (game_id) DO UPDATE SET 
               title = EXCLUDED.title,
                   description = EXCLUDED.description,
                   release_year = EXCLUDED.release_year,
                   genre = EXCLUDED.genre,
                   cover_image_url = EXCLUDED.cover_image_url
            """,
            game_row,
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def initialise_database():
    """
    Function to populate the database with some games on load, calls every other function in this file.
    """
    games = get_games_by_date()
    rows = [convert_game_to_row(game) for game in games]
    push_to_db(rows)
    print(f'Pushed {len(rows)} rows into database.')
    return
