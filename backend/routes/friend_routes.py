# Modul pentru rutele legate de prieteni (/friends, /friends/<username>/movies)
from flask import Blueprint, request, jsonify
import sqlite3
from models.database import get_db_connection
from security import verifica_token

friend_bp = Blueprint('friends', __name__)

@friend_bp.route('/friends', methods=['GET'])
def get_friends():
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    conn = get_db_connection()
    # Relatie bidirectionala: cautam atat prietenii unde user_id = id_user, cat si unde friend_id = id_user
    prieteni = conn.execute('''
        SELECT DISTINCT u.username 
        FROM users u
        INNER JOIN friends f ON (f.friend_id = u.id AND f.user_id = ?) OR (f.user_id = u.id AND f.friend_id = ?)
        WHERE u.id != ?
    ''', (id_user, id_user, id_user)).fetchall()
    
    conn.close()
    lista_prieteni = [prieten['username'] for prieten in prieteni]
    
    return jsonify(lista_prieteni), 200

@friend_bp.route('/friends/add', methods=['POST'])
def add_friend():
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    date = request.get_json()
    if not date:
        return jsonify({'message': 'Date lipsa'}), 400
    
    nume_prieten = date.get('friend_username')
    if not nume_prieten or not nume_prieten.strip():
        return jsonify({'message': 'Numele prietenului este obligatoriu'}), 400
    
    conn = get_db_connection()
    prieten = conn.execute('SELECT id FROM users WHERE username = ?', (nume_prieten,)).fetchone()
    
    if not prieten:
        conn.close()
        return jsonify({'message': 'Utilizator negasit'}), 404
    
    id_prieten = prieten['id']
    
    if id_user == id_prieten:
        conn.close()
        return jsonify({'message': 'Nu te poti adauga pe tine insuti'}), 400
    
    prietenie_existenta = conn.execute('SELECT id FROM friends WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)', 
                                      (id_user, id_prieten, id_prieten, id_user)).fetchone()
    
    if prietenie_existenta:
        conn.close()
        return jsonify({'message': 'Prietenia exista deja'}), 400
    
    try:
        # Relatie bidirectionala: inseram 2 randuri
        conn.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (id_user, id_prieten))
        conn.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (id_prieten, id_user))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Prieten adaugat'}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'message': 'Prietenia exista deja'}), 400
    except Exception:
        conn.close()
        return jsonify({'message': 'Eroare la adaugarea prietenului'}), 400

@friend_bp.route('/friends/<friend_username>/movies', methods=['GET'])
def get_friend_movies(friend_username):
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    conn = get_db_connection()
    prieten = conn.execute('SELECT id FROM users WHERE username = ?', (friend_username,)).fetchone()
    
    if not prieten:
        conn.close()
        return jsonify({'message': 'Utilizator negasit'}), 404
    
    id_prieten = prieten['id']
    
    # Verificare prietenie: utilizatorul poate vedea filmele doar daca sunt prieteni
    prietenie = conn.execute('SELECT id FROM friends WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)', 
                            (id_user, id_prieten, id_prieten, id_user)).fetchone()
    
    if not prietenie:
        conn.close()
        return jsonify({'message': 'Nu sunteti prieteni'}), 403
    
    date_filme = conn.execute('SELECT id, title, status, rating FROM movies WHERE user_id = ? ORDER BY status, title', 
                              (id_prieten,)).fetchall()
    conn.close()
    
    filme = {
        'To Watch': [],
        'Watching': [],
        'Completed': []
    }
    
    for rand in date_filme:
        status = rand['status']
        if status in filme:
            filme[status].append({
                'id': rand['id'],
                'title': rand['title'],
                'rating': rand['rating'] if rand['rating'] else '-'
            })
    
    return jsonify(filme), 200

