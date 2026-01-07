from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sys
import os

# Importam validators din utils
from utils.validators import validate_username, validate_password

# Add correct path to find api_client
CLIENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CLIENT_DIR)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
# Afiseaza pagina de login
def show_login():
    # Daca utilizatorul este deja autentificat, redirect la dashboard
    if 'token' in session:
        return redirect(url_for('dashboard.show_dashboard'))
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
# Proceseaza login-ul
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    # Validare
    valid, message = validate_username(username)
    if not valid:
        flash(message, 'error')
        return render_template('login.html')
    
    valid, message = validate_password(password)
    if not valid:
        flash(message, 'error')
        return render_template('login.html')
    
    from api_client import api_client
    
    response = api_client.post('login', {'username': username, 'password': password})
    
    if response and response.status_code == 200:
        data = response.json()
        token = data.get('token')
        
        # Set session
        session['username'] = username
        session['token'] = token
        
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard.show_dashboard'))
    else:
        flash('Invalid username or password', 'error')
        return render_template('login.html')

@auth_bp.route('/register', methods=['GET'])
# Afiseaza pagina de inregistrare
def show_register():
    if 'token' in session:
        return redirect(url_for('dashboard.show_dashboard'))
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
# Proceseaza inregistrarea
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    # Validare
    valid, message = validate_username(username)
    if not valid:
        flash(message, 'error')
        return render_template('register.html')
    
    valid, message = validate_password(password)
    if not valid:
        flash(message, 'error')
        return render_template('register.html')
    
    # Call API for registration
    from api_client import api_client
    
    response = api_client.post('register', {'username': username, 'password': password})
    
    if response is not None and response.status_code == 201:
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.show_login'))
    elif response is not None and 'message' in response.json():
        flash(response.json()['message'], 'error')
        return render_template('register.html')
    else:
        flash('Registration error', 'error')
        return render_template('register.html')

@auth_bp.route('/logout', methods=['POST'])
# Delogare utilizator
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.show_login'))
