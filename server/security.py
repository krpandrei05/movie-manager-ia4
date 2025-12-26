from functools import wraps
from flask import request, jsonify
from models.database import get_db_connection

def verifica_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        # Simulare verificare token (in realitate ar fi JWT sau DB check)
        if not token.startswith("token_secret_pentru_"):
            return jsonify({'message': 'Token is invalid!'}), 401
        
        # Extragem username din token-ul fals (format: token_secret_pentru_X)
        username = token.replace("token_secret_pentru_", "")
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if not user:
             return jsonify({'message': 'User associated with token not found'}), 401
             
        # Injectam user_id in kwargs pentru a fi folosit in ruta
        return f(user_id=user['id'], *args, **kwargs)
        
    return decorated
