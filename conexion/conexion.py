import sqlite3
from flask import g
import os

DB_FILE = os.getenv("DB_FILE", "desarrollo_web.db")

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn
