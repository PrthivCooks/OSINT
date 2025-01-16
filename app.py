from flask import Flask, request, jsonify
from flask_cors import CORS
from google_search_results import GoogleSearch
from urllib.parse import parse_qsl, urlsplit
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

SERPAPI_API_KEY = "85c261d44fa7d3f382a97b305a953bb0f58b9ab395f57b396a887cdf415235e7"  # Replace with your real API key

def fetch_news_with_serpapi(keyword, start_date=None, end_date=None, location="us"):
    """ Fetch news articles using SerpAPI with optional date filtering. """
    params = {
        "api_key": SERPAPI_API_KEY,
        "engine": "google",
        "q": keyword,
        "gl": location,
        "hl": "en",
        "num": "50",
        "tbm": "nws"  # Google News Search
    }

    # Apply date range filtering if provided
    if start_date and end_date:
        params["tbs"] = f"cdr:1,cd_min:{start_date},cd_max:{end_date}"

    search = GoogleSearch(params)
    all_results = {"name": f"News about {keyword}", "news_results": []}

    try:
        results = search.get_dict()
        if "error" in results:
            return {"error": results["error"]}

        # Extract relevant news results
        for result in results.get("news_results", []):
            news_entry = {
                "title": result.get("title"),
                "link": result.get("link"),
                "source": result.get("source"),
                "date": result.get("date"),
                "thumbnail": result.get("thumbnail")
            }
            all_results["news_results"].append(news_entry)
    
    except Exception as e:
        return {"error": str(e)}

    return all_results

@app.route('/api/news', methods=['POST'])
def get_news():
    """ API endpoint to fetch news based on keyword and filters. """
    data = request.json
    keyword = data.get('keyword', '')
    start_date = data.get('start_date', '')
    end_date = data.get('end_date', '')
    location = data.get('location', 'us')

    if not keyword:
        return jsonify({"error": "Keyword is required."}), 400

    news_data = fetch_news_with_serpapi(keyword, start_date, end_date, location)
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
