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
        
    def login(self, username, password):
        url = f"{self.base_url}/login"
        try:
            return requests.post(url, json={'username': username, 'password': password})
        except requests.exceptions.RequestException:
            return None

    def register(self, username, password):
        url = f"{self.base_url}/register"
        try:
            return requests.post(url, json={'username': username, 'password': password})
        except requests.exceptions.RequestException:
            return None
            
    def get_movies(self):
        url = f"{self.base_url}/movies"
        try:
            return requests.get(url, headers=self._get_headers())
        except requests.exceptions.RequestException:
            return None

    def add_movie(self, title, year=None, poster=None):
        url = f"{self.base_url}/movies"
        data = {'title': title, 'year': year, 'poster': poster}
        try:
            return requests.post(url, json=data, headers=self._get_headers())
        except requests.exceptions.RequestException:
            return None

    def delete_movie(self, movie_id):
        url = f"{self.base_url}/movies/{movie_id}"
        try:
            return requests.delete(url, headers=self._get_headers())
        except requests.exceptions.RequestException:
            return None
            
    def update_movie_status(self, movie_id, status):
        url = f"{self.base_url}/movies/{movie_id}"
        try:
            return requests.put(url, json={'status': status}, headers=self._get_headers())
        except requests.exceptions.RequestException:
            return None

    def get(self, endpoint):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            return requests.get(url, headers=self._get_headers())
        except requests.exceptions.RequestException:
            return None

    def post(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            return requests.post(url, json=data, headers=self._get_headers())
        except requests.exceptions.RequestException:
            return None

    def put(self, endpoint, data=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            return requests.put(url, json=data, headers=self._get_headers())
        except requests.exceptions.RequestException:
            return None

    def delete(self, endpoint):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            return requests.delete(url, headers=self._get_headers())
        except requests.exceptions.RequestException:
            return None

api_client = APIClient()