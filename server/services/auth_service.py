# Modul pentru logica de autentificare
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from models.database import get_db_connection

def proceseaza_inregistrare():
    date = request.get_json()
    if not date:
        return jsonify({"message": "Missing data"}), 400
    
    nume = date.get('username')
    parola = date.get('password')
    
    if not nume or not parola:
        return jsonify({"message": "Username and password are required"}), 400
    
    conn = get_db_connection()
    try:
        # Criptare parola
        parola_criptata = generate_password_hash(parola)
        
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (nume, parola_criptata))
        conn.commit()
        return jsonify({"message": "User created"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists"}), 400
    finally:
        conn.close()

def proceseaza_login():
    date = request.get_json()
    nume = date.get('username')
    parola = date.get('password')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (nume,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], parola):
        # Format token simplu pentru demonstratie
        return jsonify({"token": "token_secret_pentru_" + nume}), 200
    
    return jsonify({"message": "Incorrect username or password"}), 401
