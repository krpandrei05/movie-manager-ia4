from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, FRONTEND_DIR)
from utils.validators import validate_username, validate_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def show_login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.show_dashboard'))
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    valid, message = validate_username(username)
    if not valid:
        flash(message, 'error')
        return render_template('login.html')
    
    valid, message = validate_password(password)
    if not valid:
        flash(message, 'error')
        return render_template('login.html')
    
    from models.database import get_db_connection
    from werkzeug.security import check_password_hash
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = username
        session['token'] = f'token_secret_pentru_{username}'
        
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard.show_dashboard'))
    else:
        flash('Invalid username or password', 'error')
        return render_template('login.html')

@auth_bp.route('/register', methods=['GET'])
def show_register():
    if 'user_id' in session:
        return redirect(url_for('dashboard.show_dashboard'))
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    valid, message = validate_username(username)
    if not valid:
        flash(message, 'error')
        return render_template('register.html')
    
    valid, message = validate_password(password)
    if not valid:
        flash(message, 'error')
        return render_template('register.html')
    
    from models.database import get_db_connection
    from werkzeug.security import generate_password_hash
    import sqlite3
    
    conn = get_db_connection()
    try:
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                    (username, password_hash))
        conn.commit()
        conn.close()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.show_login'))
    except sqlite3.IntegrityError:
        conn.close()
        flash('Username already exists', 'error')
        return render_template('register.html')
    except Exception as e:
        conn.close()
        flash('Registration error', 'error')
        return render_template('register.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.show_login'))