# Modul pentru interogarea API-urilor externe (TVMaze pentru cautare filme)
import urllib.request
import urllib.parse
import json
from flask import request, jsonify

def search_movies():
    search_term = request.args.get('s', '')
    
    if not search_term or not search_term.strip():
        return jsonify({'Response': 'False', 'Error': 'Search term required'}), 400
    
    try:
        search_params = urllib.parse.urlencode({
            'q': search_term.strip()
        })
        tvmaze_url = f'http://api.tvmaze.com/search/shows?{search_params}'
        
        with urllib.request.urlopen(tvmaze_url, timeout=5) as response:
            data = json.loads(response.read().decode())
        
        # TVMaze returneaza lista de obiecte cu 'show' in interior, transformam in format compatibil
        formatted_results = {
            'Response': 'True',
            'Search': []
        }
        
        for item in data:
            show = item.get('show', {})
            formatted_results['Search'].append({
                'Title': show.get('name', 'Unknown'),
                # Extragem anul din data de premiere (ex: "2010-01-15" -> "2010")
                'Year': show.get('premiered', '')[:4] if show.get('premiered') else 'N/A',
                'Type': show.get('type', 'show'),
                'imdbID': str(show.get('id', '')),
                'Poster': show.get('image', {}).get('medium', '') if show.get('image') else ''
            })
        
        return jsonify(formatted_results), 200
    except Exception as e:
        return jsonify({'Response': 'False', 'Error': 'Error searching movies'}), 500

