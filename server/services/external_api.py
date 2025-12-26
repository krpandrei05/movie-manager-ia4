import requests
from flask import jsonify, request

def search_movies():
    query = request.args.get('q')
    if not query:
        return jsonify([])

    try:
        # Interogare TVMaze API
        response = requests.get(f"https://api.tvmaze.com/search/shows?q={query}")
        if response.status_code == 200:
            results = response.json()
            # Formatam datele pentru frontend
            formatted_results = []
            for item in results:
                show = item.get('show', {})
                image = show.get('image', {})
                formatted_results.append({
                    'title': show.get('name'),
                    'year': show.get('premiered', '')[:4] if show.get('premiered') else '',
                    'poster': image.get('medium') if image else None
                })
            return jsonify(formatted_results)
        return jsonify([])
    except Exception as e:
        print(f"Error searching TVMaze: {e}")
        return jsonify([])