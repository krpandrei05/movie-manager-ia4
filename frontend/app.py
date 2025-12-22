from flask import Flask, redirect, url_for, session
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'movie_manager_secret_key_change_in_production'

from views import auth_views

app.register_blueprint(auth_views.auth_bp)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard.show_dashboard'))
    return redirect(url_for('auth.show_login'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)