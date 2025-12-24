from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from api_client import APIClient

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def show_dashboard():
    if 'token' not in session:
        return redirect(url_for('auth.login'))
        
    client = APIClient()
    response = client.get_movies()
    
    movies = []
    if response and response.status_code == 200:
        movies = response.json()
    else:
        flash("Could not load movies.", "error")
        
    return render_template('dashboard.html', movies=movies, user=session.get('user'))

@dashboard_bp.route('/movies/add', methods=['POST'])
def add_movie():
    if 'token' not in session:
        return redirect(url_for('auth.login'))
        
    title = request.form.get('title')
    year = request.form.get('year')
    poster = request.form.get('poster')
    
    if not title:
        flash('Title is required', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
        
    client = APIClient()
    response = client.add_movie(title, year, poster)
    
    if response and response.status_code == 201:
        flash('Movie added successfully!', 'success')
    else:
        flash('Error adding movie', 'error')
        
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    if 'token' not in session:
        return redirect(url_for('auth.login'))
        
    client = APIClient()
    response = client.delete_movie(movie_id)
    
    if response and response.status_code == 200:
        flash('Movie deleted', 'success')
    else:
        flash('Error deleting movie', 'error')
        
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/status/<int:movie_id>', methods=['POST'])
def update_status(movie_id):
    if 'token' not in session:
        return redirect(url_for('auth.login'))
        
    new_status = request.form.get('status')
    client = APIClient()
    client.update_movie_status(movie_id, new_status)
    
    return redirect(url_for('dashboard.show_dashboard'))
