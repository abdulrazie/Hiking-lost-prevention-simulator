import sqlite3
from pathlib import Path

database_file = Path(__file__).with_name("hikers.db")


def get_connection():
    connection = sqlite3.connect(database_file)

    connection.row_factory = sqlite3.Row

    return connection