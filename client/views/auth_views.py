from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from api_client import APIClient

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        client = APIClient()
        response = client.register(username, password)
        
        if response and response.status_code == 201:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            message = "Registration failed"
            if response:
                try:
                    message = response.json().get('message', message)
                except:
                    pass
            flash(message, 'error')
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        client = APIClient()
        response = client.login(username, password)
        
        if response and response.status_code == 200:
            token = response.json().get('token')
            session['user'] = username
            session['token'] = token
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('index')) # Va fi dashboard
        else:
            flash('Invalid credentials', 'error')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
