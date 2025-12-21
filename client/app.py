from flask import Flask, redirect, url_for, session
import os
import sys

# Initializam aplicatia Flask pentru frontend
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'movie_manager_secret_key_change_in_production'  # Pentru sessions

@app.route('/')
def index():
    # Placeholder pana implementam auth
    return "Client App Running! (Waiting for Auth implementation)"

if __name__ == '__main__':
    app.run(debug=True, port=5001)