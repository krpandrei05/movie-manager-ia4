from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

from models.database import get_db_connection

FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FRONTEND_DIR)
from utils.validators import validate_username

friend_bp = Blueprint('friend', __name__)

def require_auth():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.show_login'))
    return None

@friend_bp.route('/friends')
def show_friends():
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    
    conn = get_db_connection()
    friends_data = conn.execute('''
        SELECT DISTINCT u.username 
        FROM users u
        INNER JOIN friends f ON (f.friend_id = u.id AND f.user_id = ?) OR (f.user_id = u.id AND f.friend_id = ?)
        WHERE u.id != ?
    ''', (user_id, user_id, user_id)).fetchall()
    conn.close()
    
    friends = [friend['username'] for friend in friends_data]
    
    return render_template('friends.html', friends=friends)

@friend_bp.route('/friends/add', methods=['POST'])
def add_friend():
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    friend_username = request.form.get('friend_username', '').strip()
    
    valid, message = validate_username(friend_username)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('friend.show_friends'))
    
    conn = get_db_connection()
    
    friend_user = conn.execute('SELECT id FROM users WHERE username = ?', (friend_username,)).fetchone()
    
    if not friend_user:
        conn.close()
        flash('User not found', 'error')
        return redirect(url_for('friend.show_friends'))
    
    friend_id = friend_user['id']
    
    if user_id == friend_id:
        conn.close()
        flash('You cannot add yourself', 'error')
        return redirect(url_for('friend.show_friends'))
    
    existing = conn.execute('''
        SELECT id FROM friends 
        WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
    ''', (user_id, friend_id, friend_id, user_id)).fetchone()
    
    if existing:
        conn.close()
        flash('Friendship already exists', 'error')
        return redirect(url_for('friend.show_friends'))
    
    try:
        conn.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (user_id, friend_id))
        conn.execute('INSERT INTO friends (user_id, friend_id) VALUES (?, ?)', (friend_id, user_id))
        conn.commit()
        conn.close()
        flash('Friend added successfully!', 'success')
    except Exception as e:
        conn.close()
        flash('Error adding friend', 'error')
    
    return redirect(url_for('friend.show_friends'))

@friend_bp.route('/friends/<username>')
def show_friend_profile(username):
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    user_id = session['user_id']
    
    conn = get_db_connection()
    friend_user = conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    
    if not friend_user:
        conn.close()
        flash('User not found', 'error')
        return redirect(url_for('friend.show_friends'))
    
    friend_id = friend_user['id']
    
    friendship = conn.execute('''
        SELECT id FROM friends 
        WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
    ''', (user_id, friend_id, friend_id, user_id)).fetchone()
    
    if not friendship:
        conn.close()
        flash('You are not friends with this user', 'error')
        return redirect(url_for('friend.show_friends'))
    
    movies_data = conn.execute(
        'SELECT id, title, status, rating FROM movies WHERE user_id = ? ORDER BY status, title',
        (friend_id,)
    ).fetchall()
    conn.close()
    
    movies = {'To Watch': [], 'Watching': [], 'Completed': []}
    for row in movies_data:
        status = row['status']
        if status in movies:
            rating = row['rating'] if row['rating'] and row['rating'] != '-' else None
            movies[status].append({
                'id': row['id'],
                'title': row['title'],
                'rating': rating
            })
    
    return render_template('friend_profile.html', friend_username=username, movies=movies)
