from flask import Blueprint, request, jsonify
from models.database import get_db_connection
from security import verifica_token

movie_bp = Blueprint('movie_api', __name__)

@movie_bp.route('/movies', methods=['GET'])
@verifica_token
def get_movies(user_id):
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM movies WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    
    movies_list = [dict(movie) for movie in movies]
    return jsonify(movies_list), 200

@movie_bp.route('/movies', methods=['POST'])
@verifica_token
def add_movie(user_id):
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'message': 'Title is required'}), 400
        
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO movies (user_id, title, year, poster, status) VALUES (?, ?, ?, ?, ?)',
        (user_id, data['title'], data.get('year'), data.get('poster'), data.get('status', 'To Watch'))
    )
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Movie added successfully'}), 201

@movie_bp.route('/movies/<int:movie_id>', methods=['DELETE'])
@verifica_token
def delete_movie(user_id, movie_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM movies WHERE id = ? AND user_id = ?', (movie_id, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Movie deleted successfully'}), 200

@movie_bp.route('/movies/<int:movie_id>', methods=['PUT'])
@verifica_token
def update_movie(user_id, movie_id):
    data = request.get_json()
    status = data.get('status')
    
    if not status:
        return jsonify({'message': 'Status is required'}), 400
        
    conn = get_db_connection()
    conn.execute('UPDATE movies SET status = ? WHERE id = ? AND user_id = ?', (status, movie_id, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Movie updated successfully'}), 200
