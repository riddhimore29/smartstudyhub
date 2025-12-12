from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import concurrent.futures

# Import providers
from providers.wikipedia import fetch_wikipedia
from providers.duckduckgo import fetch_duckduckgo
from providers.piped import fetch_piped

# Import ranking logic
from ranking import rank_resources

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app) # Enable CORS for all routes

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/search.html')
def search_page():
    return send_from_directory(app.static_folder, 'search.html')

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q')
    filter_type = request.args.get('filter', 'all').lower()
    
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    print(f"Searching for: {query} [Filter: {filter_type}]")

    # Fetch data concurrently from all providers
    all_resources = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_wiki = executor.submit(fetch_wikipedia, query)
        future_ddg = executor.submit(fetch_duckduckgo, query)
        future_piped = executor.submit(fetch_piped, query)
        
        # Collect results
        wiki_res = future_wiki.result()
        ddg_res = future_ddg.result()
        piped_res = future_piped.result()
        
        all_resources.extend(wiki_res)
        all_resources.extend(ddg_res)
        all_resources.extend(piped_res)

    print(f"Stats: Wiki={len(wiki_res)}, DDG={len(ddg_res)}, Piped={len(piped_res)}")
    print(f"Fetched {len(all_resources)} raw resources.")
    
    # Rank and filter resources
    top_resources = rank_resources(query, all_resources, filter_type)
    
    # Debug stats
    debug_stats = {
        "piped_count": len(piped_res),
        "ddg_count": len(ddg_res),
        "wiki_found": len(wiki_res) > 0,
        "total_raw": len(all_resources)
    }
    print(f"Stats: {debug_stats}") # Log to backend stdout

    return jsonify({
        "query": query,
        "filter": filter_type,
        "debug": debug_stats,
        "results": top_resources
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
