from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sys
import os

# Importam validators din utils
# Assuming utils is in the path
from utils.validators import validate_movie_title, validate_rating

# Add correct path to find api_client
CLIENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CLIENT_DIR)

dashboard_bp = Blueprint('dashboard', __name__)

# Verifica daca utilizatorul este autentificat
def require_auth():
    if 'token' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.show_login'))
    return None


@dashboard_bp.route('/dashboard')
# Afiseaza dashboard-ul cu filmele utilizatorului
def show_dashboard():
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    username = session.get('username', 'User')
    
    from api_client import api_client
    
    movies_response = api_client.get('movies')
    if movies_response and movies_response.status_code == 200:
        movies = movies_response.json()
    else:
        movies = {'To Watch': [], 'Watching': [], 'Completed': []}
        flash('Error fetching movies', 'error')

    friends_response = api_client.get('friends')
    if friends_response and friends_response.status_code == 200:
        friends = friends_response.json()
    else:
        friends = []
    
    return render_template('dashboard.html', movies=movies, username=username, friends=friends)

@dashboard_bp.route('/movies/add', methods=['POST'])
# Adauga un film nou
def add_movie():
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    title = request.form.get('title', '').strip()
    status = request.form.get('status', 'To Watch')
    movie_validated = request.form.get('movie_validated', '0')
    
    # Validare stricta: verificam daca filmul a fost selectat din dropdown
    if movie_validated != '1':
        flash('Please select a movie from the dropdown list.', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Validare titlu
    valid, message = validate_movie_title(title)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Verificam statusul
    if status not in ['To Watch', 'Watching', 'Completed']:
        status = 'To Watch'
    
    # Call API to add movie
    from api_client import api_client
    
    response = api_client.post('movies', {'title': title, 'status': status})
    
    if response and response.status_code == 201:
        flash('Movie added successfully!', 'success')
    elif response and 'message' in response.json():
        flash(response.json()['message'], 'error')
    else:
        flash('Error adding movie', 'error')
    
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/<int:movie_id>/move', methods=['POST'])
# Muta un film intre liste
def move_movie(movie_id):
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    new_status = request.form.get('new_list', '').strip()
    
    if new_status not in ['To Watch', 'Watching', 'Completed']:
        flash('Invalid status', 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Call API to move movie
    from api_client import api_client
    
    response = api_client.put(f'movies/{movie_id}/move', {'new_list': new_status})
    
    if response and response.status_code == 200:
        flash(f'Movie moved to {new_status} successfully!', 'success')
    else:
        if response and response.status_code == 404:
            flash('Movie not found', 'error')
        else:
            flash('Error moving movie', 'error')
            
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/<int:movie_id>/rate', methods=['POST'])
# Noteaza un film
def rate_movie(movie_id):
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    rating = request.form.get('rating', '').strip()
    
    # Validare
    valid, message = validate_rating(rating)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('dashboard.show_dashboard'))
    
    # Call API to rate movie
    from api_client import api_client
    
    response = api_client.put(f'movies/{movie_id}/rate', {'rating': rating})
    
    if response and response.status_code == 200:
        flash(f'Movie rated {rating}/10!', 'success')
    else:
        if response and response.status_code == 404:
            flash('Movie not found', 'error')
        else:
            flash('Error rating movie', 'error')
    
    return redirect(url_for('dashboard.show_dashboard'))

@dashboard_bp.route('/movies/<int:movie_id>/delete', methods=['POST'])
# Sterge un film
def delete_movie(movie_id):
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    
    # Call API to delete movie - using DELETE method
    from api_client import api_client
    
    response = api_client.delete(f'movies/{movie_id}')
    
    if response and response.status_code == 200:
        flash('Movie deleted successfully!', 'success')
    else:
        # If 404 or other error, handle gracefully
        if response and response.status_code == 404:
             flash('Movie not found', 'error')
        else:
             flash('Error deleting movie', 'error')
    
    return redirect(url_for('dashboard.show_dashboard'))
