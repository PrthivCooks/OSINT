from flask import Flask, request, jsonify
from flask_cors import CORS
from serpapi import GoogleSearch  # Correct import for Python SerpAPI

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

SERPAPI_API_KEY = "85c261d44fa7d3f382a97b305a953bb0f58b9ab395f57b396a887cdf415235e7"

def fetch_news_with_serpapi(keyword, location="us"):
    """ Fetch news articles using SerpAPI's Google News Engine. """
    params = {
        "engine": "google_news",
        "q": keyword,
        "gl": location,  # Geolocation (Country Code)
        "hl": "en",  # Language (English)
        "api_key": SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()  # Get results as dictionary

    # Extract and structure news results
    if "news_results" in results:
        return {
            "name": f"News about {keyword}",
            "news_results": [
                {
                    "title": article.get("title"),
                    "link": article.get("link"),
                    "source": article.get("source"),
                    "date": article.get("date"),
                    "thumbnail": article.get("thumbnail"),
                }
                for article in results["news_results"]
            ]
        }
    else:
        return {"error": "No news results found."}

@app.route('/api/news', methods=['POST'])
def get_news():
    """ API endpoint to fetch Google News based on a keyword. """
    data = request.json
    keyword = data.get('keyword', '')
    location = data.get('location', 'us')

    if not keyword:
        return jsonify({"error": "Keyword is required."}), 400

    news_data = fetch_news_with_serpapi(keyword, location)
    return jsonify(news_data)

@app.route('/')
def index():
    """ Root endpoint to confirm the API is running. """
    return jsonify({
        "message": "Python Backend API Running!",
        "routes": ["/api/news (POST) - Fetch Google News"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
