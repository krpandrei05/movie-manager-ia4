from flask import Flask, redirect, url_for, session
import os
import sys

# Initializam aplicatia Flask pentru frontend
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'movie_manager_secret_key_change_in_production' 

# Import View Handlers
from views import auth_views
from views import dashboard_views

# Register Blueprints
app.register_blueprint(auth_views.auth_bp)
app.register_blueprint(dashboard_views.dashboard_bp)

@app.route('/')
def index():
    # Daca e logat il trimitem la dashboard
    if 'token' in session:
        return redirect(url_for('dashboard.show_dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)