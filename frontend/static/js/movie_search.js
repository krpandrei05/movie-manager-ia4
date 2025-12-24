const MOVIE_SEARCH_URL = 'http://localhost:5000/api/search-movies';

let searchTimeout = null;
let currentSearchResults = [];

let selectedMovieDashboard = null;
let selectedMovieRecommend = null;

function searchMovies(searchTerm) {
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    if (!searchTerm || searchTerm.trim().length < 2) {
        hideSearchResults();
        selectedMovieDashboard = null;
        return;
    }
    
    searchTimeout = setTimeout(async () => {
        try {
            const response = await fetch(`${MOVIE_SEARCH_URL}?s=${encodeURIComponent(searchTerm.trim())}`);
            const data = await response.json();
            
            if (data.Response === 'True' && data.Search) {
                currentSearchResults = data.Search;
                displaySearchResults(currentSearchResults, 'movie-search-results');
            } else {
                const resultsDiv = document.getElementById('movie-search-results');
                if (resultsDiv) {
                    resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
                    resultsDiv.classList.add('show');
                }
            }
        } catch (error) {
            const resultsDiv = document.getElementById('movie-search-results');
            if (resultsDiv) {
                resultsDiv.innerHTML = '<div class="movie-search-error">Error searching movies</div>';
                resultsDiv.classList.add('show');
            }
        }
    }, 300);
}

function searchMoviesRecommend(searchTerm) {
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }
    
    if (!searchTerm || searchTerm.trim().length < 2) {
        hideSearchResultsRecommend();
        selectedMovieRecommend = null;
        return;
    }
    
    searchTimeout = setTimeout(async () => {
        try {
            const response = await fetch(`${MOVIE_SEARCH_URL}?s=${encodeURIComponent(searchTerm.trim())}`);
            const data = await response.json();
            
            if (data.Response === 'True' && data.Search) {
                currentSearchResults = data.Search;
                displaySearchResults(currentSearchResults, 'movie-search-results-recommend');
            } else {
                const resultsDiv = document.getElementById('movie-search-results-recommend');
                if (resultsDiv) {
                    resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
                    resultsDiv.classList.add('show');
                }
            }
        } catch (error) {
            const resultsDiv = document.getElementById('movie-search-results-recommend');
            if (resultsDiv) {
                resultsDiv.innerHTML = '<div class="movie-search-error">Error searching movies</div>';
                resultsDiv.classList.add('show');
            }
        }
    }, 300);
}

function displaySearchResults(results, containerId) {
    const resultsDiv = document.getElementById(containerId);
    
    if (!resultsDiv) {
        return;
    }
    
    if (!results || results.length === 0) {
        resultsDiv.innerHTML = '<div class="movie-search-error">No movies found</div>';
        resultsDiv.classList.add('show');
        return;
    }
    
    resultsDiv.innerHTML = results.map((movie, index) => {
        const titleEscaped = movie.Title.replace(/'/g, "\\'").replace(/"/g, '&quot;');
        const titleHtml = movie.Title.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const yearHtml = (movie.Year || 'N/A').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        const typeHtml = (movie.Type || 'show').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
        return `
            <div class="movie-search-item" onclick="selectMovie('${titleEscaped}', '${containerId}')">
                <div class="movie-title">${titleHtml}</div>
                <div class="movie-year">${yearHtml}</div>
                <div class="movie-type">${typeHtml}</div>
            </div>
        `;
    }).join('');
    
    resultsDiv.classList.add('show');
}

function selectMovie(movieTitle, containerId) {
    const selectedMovie = currentSearchResults.find(movie => movie.Title === movieTitle);
    
    if (containerId === 'movie-search-results') {
        const input = document.getElementById('movie-title');
        if (input) {
            input.value = movieTitle;
            selectedMovieDashboard = selectedMovie;
            const hiddenInput = document.getElementById('movie-validated');
            if (hiddenInput) {
                hiddenInput.value = '1';
            }
        }
    } else if (containerId === 'movie-search-results-recommend') {
        const input = document.getElementById('recommend-movie-title');
        if (input) {
            input.value = movieTitle;
            selectedMovieRecommend = selectedMovie;
            const hiddenInput = document.getElementById('recommend-movie-validated');
            if (hiddenInput) {
                hiddenInput.value = '1';
            }
        }
    }
    
    hideSearchResults();
    hideSearchResultsRecommend();
}

function showSearchResults() {
    const input = document.getElementById('movie-title');
    if (input) {
        const searchTerm = input.value;
        if (searchTerm && searchTerm.trim().length >= 2 && currentSearchResults.length > 0) {
            const resultsDiv = document.getElementById('movie-search-results');
            if (resultsDiv) {
                resultsDiv.classList.add('show');
            }
        }
    }
}

function hideSearchResults() {
    setTimeout(() => {
        const resultsDiv = document.getElementById('movie-search-results');
        if (resultsDiv) {
            resultsDiv.classList.remove('show');
        }
    }, 200);
}

function showSearchResultsRecommend() {
    const input = document.getElementById('recommend-movie-title');
    if (input) {
        const searchTerm = input.value;
        if (searchTerm && searchTerm.trim().length >= 2 && currentSearchResults.length > 0) {
            const resultsDiv = document.getElementById('movie-search-results-recommend');
            if (resultsDiv) {
                resultsDiv.classList.add('show');
            }
        }
    }
}

function hideSearchResultsRecommend() {
    setTimeout(() => {
        const resultsDiv = document.getElementById('movie-search-results-recommend');
        if (resultsDiv) {
            resultsDiv.classList.remove('show');
        }
    }, 200);
}

