import requests

def fetch_wikipedia(query):
    """
    Fetches Wikipedia articles with comprehensive search to return 5-10 results.
    """
    try:
        headers = {
            "User-Agent": "SmartStudyHub/1.0 (Educational; contact@example.com)"
        }
        
        # Use Wikipedia's opensearch API (returns multiple results)
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "opensearch",
            "search": query,
            "limit": 10,  # Get up to 10 results
            "namespace": 0,  # Main namespace only (articles)
            "format": "json"
        }
        
        search_response = requests.get(search_url, params=search_params, headers=headers, timeout=4)
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            # Format: [query, [titles], [descriptions], [urls]]
            
            if len(search_data) >= 4 and search_data[1]:
                results = []
                titles = search_data[1]
                descriptions = search_data[2]
                urls = search_data[3]
                
                for i in range(min(len(titles), 10)):
                    # Skip disambiguation pages
                    if "(disambiguation)" in titles[i].lower():
                        continue
                    
                    desc = descriptions[i] if i < len(descriptions) else ""
                    if not desc:
                        desc = f"Wikipedia article about {titles[i]}"
                    
                    results.append({
                        "title": titles[i],
                        "url": urls[i] if i < len(urls) else f"https://en.wikipedia.org/wiki/{titles[i].replace(' ', '_')}",
                        "type": "article",
                        "description": desc,
                        "source": "Wikipedia",
                        "duration": 0
                    })
                
                print(f"Wikipedia: Found {len(results)} articles")
                return results
        
        print("Wikipedia: No results found")
        return []
        
    except Exception as e:
        print(f"Wikipedia API Error: {e}")
        return []
