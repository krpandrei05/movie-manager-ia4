from flask import Flask, redirect, url_for, session
import os
import sys

# Initializam aplicatia Flask pentru frontend
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'movie_manager_secret_key_change_in_production'  # Pentru sessions

# Importam view handlers
from views import auth_views
from views import dashboard_views
from views import friend_views

# Inregistram blueprint-urile pentru views
app.register_blueprint(auth_views.auth_bp)
app.register_blueprint(dashboard_views.dashboard_bp)
app.register_blueprint(friend_views.friend_bp)

# Ruta root - redirect la login sau dashboard
@app.route('/')
# Redirect la login sau dashboard in functie de autentificare
def index():
    return redirect(url_for('dashboard.show_dashboard'))


# Pornim aplicatia
if __name__ == '__main__':
    # Pornim serverul Flask pe portul 5001 (backend ruleaza pe 5000)
    app.run(debug=True, port=5001)