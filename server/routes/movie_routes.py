# Modul pentru rutele legate de filme (/movies, /movies/<id>)
from flask import Blueprint, request, jsonify
from models.database import get_db_connection
from security import verifica_token

movie_bp = Blueprint('movies', __name__)

@movie_bp.route('/movies', methods=['GET'])
def get_movies():
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    baza = get_db_connection()
    date_filme = baza.execute('SELECT id, title, status FROM movies WHERE user_id = ?', (id_user,)).fetchall()
    baza.close()
    
    liste = {'To Watch': [], 'Watching': [], 'Completed': []}
    for rand in date_filme:
        status_film = rand['status']
        if status_film in liste:
            liste[status_film].append({
                'id': rand['id'], 
                'title': rand['title'],
                'year': rand['year'] if 'year' in rand.keys() else '',
                'poster': rand['poster'] if 'poster' in rand.keys() else ''
            })

    return jsonify(liste), 200

@movie_bp.route('/movies', methods=['POST'])
def add_movie():
    token = request.headers.get('Authorization')
    id_user = verifica_token(token)
    if not id_user:
        return jsonify({'message': 'Acces interzis'}), 401
    
    date = request.get_json()
    if not date:
        return jsonify({'message': 'Date lipsa'}), 400
    
    titlu = date.get('title')
    year = date.get('year')
    poster = date.get('poster')
    
    if not titlu or not titlu.strip():
        return jsonify({'message': 'Titlul este obligatoriu'}), 400
    
    # Default status
    status_ales = 'To Watch'
    
    baza = get_db_connection()
    baza.execute('INSERT INTO movies (user_id, title, year, poster, status) VALUES (?, ?, ?, ?, ?)', 
                 (id_user, titlu, year, poster, status_ales))
    baza.commit()
    baza.close()
    
    return jsonify({'message': 'Film adaugat'}), 201

@movie_bp.route('/movies/<int:id_film>', methods=['DELETE'])
def delete_movie(id_film):
    token = request.headers.get('Authorization')
    uid = verifica_token(token)
    if not uid:
        return jsonify({'message': 'Acces interzis'}), 401
    
    conn = get_db_connection()
    film = conn.execute('SELECT id FROM movies WHERE id = ? AND user_id = ?', (id_film, uid)).fetchone()
    if not film:
        conn.close()
        return jsonify({'message': 'Film negasit'}), 404
    
    conn.execute('DELETE FROM movies WHERE id = ? AND user_id = ?', (id_film, uid))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Film sters'}), 200

@movie_bp.route('/movies/<int:id_film>', methods=['PUT'])
def update_movie(id_film):
    token = request.headers.get('Authorization')
    uid = verifica_token(token)
    if not uid:
        return jsonify({'message': 'Acces interzis'}), 401
        
    date = request.get_json()
    new_status = date.get('status')
    
    if new_status:
        conn = get_db_connection()
        conn.execute('UPDATE movies SET status = ? WHERE id = ? AND user_id = ?', (new_status, id_film, uid))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Status actualizat'}), 200
        
    return jsonify({'message': 'Nimic de actualizat'}), 400