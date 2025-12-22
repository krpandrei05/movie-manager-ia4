from flask import Flask, redirect, url_for, session
import os
import sys

# Initializam aplicatia Flask pentru frontend
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'movie_manager_secret_key_change_in_production'  # Pentru sessions

# Import View Handlers
from views import auth_views

# Register Blueprints
app.register_blueprint(auth_views.auth_bp)

@app.route('/')
def index():
    if 'user' in session:
        return f"Hello {session['user']}! Dashboard coming soon... <a href='/logout'>Logout</a>"
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)