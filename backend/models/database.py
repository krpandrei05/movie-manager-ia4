# Modul pentru gestionarea bazei de date SQLite
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'production.db')

def get_db_connection():
    # Deschide o conexiune la baza de date SQLite
    # Returneaza: conexiunea configurata cu row_factory
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Initializeaza baza de date creand toate tabelele necesare
    conn = get_db_connection()
    
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, status TEXT, rating TEXT)')
    
    # Relatie bidirectionala: se insereaza 2 randuri pentru fiecare prietenie
    conn.execute('CREATE TABLE IF NOT EXISTS friends (id INTEGER PRIMARY KEY, user_id INTEGER, friend_id INTEGER, UNIQUE(user_id, friend_id))')
    
    conn.execute('CREATE TABLE IF NOT EXISTS recommendations (id INTEGER PRIMARY KEY, from_user_id INTEGER, to_user_id INTEGER, movie_title TEXT)')
    
    conn.commit()
    conn.close()

