# Backend API - Flask app pentru API REST (JSON responses)
from flask import Flask, jsonify, request
from models.database import init_db

app = Flask(__name__)

# CORS headers: permite request-uri cross-origin (frontend pe port 5001, backend pe 5000)
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

# Preflight requests: browser-ul trimite OPTIONS inainte de request-uri complexe (POST, PUT, DELETE)
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

# Inregistrare blueprint-uri cu prefix /api
# Blueprint-urile vor fi inregistrate pe masura ce sunt create

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

