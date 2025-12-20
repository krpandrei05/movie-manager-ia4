import requests
from flask import session

class APIClient:
    def __init__(self, base_url='http://localhost:5000/api'):
        self.base_url = base_url

    def _get_headers(self):
        headers = {'Content-Type': 'application/json'}
        if 'token' in session:
            headers['Authorization'] = session['token']
        return headers