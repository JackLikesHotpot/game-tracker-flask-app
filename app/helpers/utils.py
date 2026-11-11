import psycopg
import os
from psycopg.rows import dict_row

def generate_db_conn():
    """
    Helper function to create a connection to the database and returns rows as a dictionary.
    Function usable by other files.
    """
    return psycopg.connect(os.environ.get('DATABASE_URL'), row_factory=dict_row)
