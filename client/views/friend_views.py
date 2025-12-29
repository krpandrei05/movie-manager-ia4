from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sys
import os

# Importam validators din utils
# Assuming utils is in the path
from utils.validators import validate_username, validate_movie_title

# Add correct path to find api_client
CLIENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, CLIENT_DIR)

friend_bp = Blueprint('friend', __name__)

# Verifica daca utilizatorul este autentificat
def require_auth():
    if 'token' not in session:
        flash('Please login first', 'error')
        return redirect(url_for('auth.show_login'))
    return None

@friend_bp.route('/friends')
# Afiseaza pagina de prieteni
def show_friends():
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    
    # Obtinem lista de prieteni
    # Fetch friends via API
    from api_client import api_client
    
    response = api_client.get('friends')
    if response and response.status_code == 200:
        friends = response.json()
    else:
        friends = []
        flash('Error fetching friends', 'error')
    
    # API returns a list of strings (usernames), so we don't need to process it further
    # files_data = ... (removed)
    pass
    
    return render_template('friends.html', friends=friends)

@friend_bp.route('/friends/add', methods=['POST'])
# Adauga un prieten
def add_friend():
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    friend_username = request.form.get('friend_username', '').strip()
    
    # Validare
    valid, message = validate_username(friend_username)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('friend.show_friends'))
    
    # Call API to add friend
    from api_client import api_client
    
    response = api_client.post('friends/add', {'friend_username': friend_username})
    
    if response and response.status_code == 201:
        flash('Friend added successfully!', 'success')
    else:
        if response and 'message' in response.json():
            flash(response.json()['message'], 'error')
        else:
            flash('Error adding friend', 'error')
    
    return redirect(url_for('friend.show_friends'))

@friend_bp.route('/friends/<username>')
# Afiseaza profilul unui prieten
def show_friend_profile(username):
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    
    # Verificam daca prietenia exista
    # Fetch friend movies via API
    from api_client import api_client
    
    response = api_client.get(f'friends/{username}/movies')
    
    if response and response.status_code == 200:
        movies = response.json()
    else:
        if response and response.status_code == 404:
            flash('User not found', 'error')
        elif response and response.status_code == 403:
             flash('You are not friends with this user', 'error')
        else:
             flash('Error fetching friend profile', 'error')
        return redirect(url_for('friend.show_friends'))
    
    return render_template('friend_profile.html', friend_username=username, movies=movies)

@friend_bp.route('/friends/<username>/recommend', methods=['POST'])
# Recomanda un film unui prieten
def recommend_movie(username):
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    movie_title = request.form.get('movie_title', '').strip()
    movie_validated = request.form.get('movie_validated', '0')
    
    # Validare stricta: verificam daca filmul a fost selectat din dropdown
    if movie_validated != '1':
        flash('Please select a movie from the dropdown list.', 'error')
        return redirect(url_for('friend.show_friend_profile', username=username))
    
    # Validare titlu
    valid, message = validate_movie_title(movie_title)
    if not valid:
        flash(message, 'error')
        return redirect(url_for('friend.show_friend_profile', username=username))
    
    # Call API to recommend movie
    from api_client import api_client
    
    response = api_client.post('friends/recommend', {'friend_username': username, 'movie_title': movie_title})
    
    if response and response.status_code == 201:
        flash('Recommendation sent successfully!', 'success')
    else:
        if response and 'message' in response.json():
             flash(response.json()['message'], 'error')
        else:
             flash('Error sending recommendation', 'error')
    
    return redirect(url_for('friend.show_friend_profile', username=username))

@friend_bp.route('/recommendations')
# Afiseaza recomandarile primite
def show_recommendations():
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    
    # Call API to get recommendations
    from api_client import api_client
    
    response = api_client.get('recommendations')
    if response and response.status_code == 200:
        recommendations = response.json()
    else:
        recommendations = []
        flash('Error fetching recommendations', 'error')
    
    return render_template('recommendations.html', recommendations=recommendations)

@friend_bp.route('/recommendations/<int:recommendation_id>/delete', methods=['POST'])
# Sterge o recomandare
def delete_recommendation(recommendation_id):
    auth_check = require_auth()
    if auth_check:
        return auth_check
    
    # user_id = session['user_id']
    
    # Call API to delete recommendation
    from api_client import api_client
    
    response = api_client.delete(f'recommendations/{recommendation_id}')
    
    if response and response.status_code == 200:
        flash('Recommendation deleted successfully!', 'success')
    else:
        if response and response.status_code == 404:
            flash('Recommendation not found', 'error')
        else:
            flash('Error deleting recommendation', 'error')
    
    return redirect(url_for('friend.show_recommendations'))
