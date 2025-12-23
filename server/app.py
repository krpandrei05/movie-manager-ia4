# Backend API - Aplicatie Flask pentru API REST (raspunsuri JSON)
from flask import Flask, jsonify, request
from models.database import init_db
from routes.auth_routes import auth_bp
from routes.movie_routes import movie_bp

app = Flask(__name__)

# CORS headers: permite cereri cross-origin
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Preflight requests: gestioneaza cererile OPTIONS
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

# Inregistrare blueprint-uri
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(movie_bp, url_prefix='/api')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
