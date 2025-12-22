# Modul pentru logica pentru autentificare
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
    
    if not nume.strip() or not parola.strip():
        return jsonify({"message": "Username and password cannot be empty"}), 400
    
    conn = get_db_connection()
    try:
        # Criptare parola cu Werkzeug (hash securizat)
        parola_criptata = generate_password_hash(parola)
        
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (nume, parola_criptata))
        conn.commit()
        return jsonify({"message": "User created"}), 201
    except sqlite3.IntegrityError:
        # Username-ul este unic, deci daca exista deja -> eroare
        return jsonify({"message": "Username already exists"}), 400
    except Exception:
        return jsonify({"message": "Registration error"}), 400
    finally:
        conn.close()

def proceseaza_login():
    date = request.get_json()
    if not date:
        return jsonify({"message": "Missing data"}), 400
    
    nume = date.get('username')
    parola = date.get('password')
    
    if not nume or not parola:
        return jsonify({"message": "Username and password are required"}), 400
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (nume,)).fetchone()
    conn.close()
    
    if user:
        # Verificare parola: comparam hash-ul stocat cu parola introdusa
        if check_password_hash(user['password'], parola):
            # Format token: token_secret_pentru_<username>
            return jsonify({"token": "token_secret_pentru_" + nume}), 200
    
    return jsonify({"message": "Incorrect username or password"}), 401

