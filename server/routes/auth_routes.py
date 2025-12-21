from flask import Blueprint, request, jsonify
from services.auth_service import proceseaza_inregistrare, proceseaza_login

auth_bp = Blueprint('auth_api', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    return proceseaza_inregistrare()

@auth_bp.route('/login', methods=['POST'])
def login():
    return proceseaza_login()
