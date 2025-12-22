# Modul pentru rutele de autentificare (/login, /register)
from flask import Blueprint
from services.auth_service import proceseaza_inregistrare, proceseaza_login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    # Delegare logica catre auth_service
    return proceseaza_inregistrare()

@auth_bp.route('/login', methods=['POST'])
def login():
    # Delegare logica catre auth_service
    return proceseaza_login()

