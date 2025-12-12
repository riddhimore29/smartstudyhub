import requests
import xml.etree.ElementTree as ET
import urllib.parse

# Educational YouTube channels for different topics
EDUCATIONAL_CHANNELS = {
    "math": ["3Blue1Brown", "Numberphile", "Khan Academy", "Mathologer"],
    "science": ["Kurzgesagt", "Vsauce", "Veritasium", "SmarterEveryDay"],
    "programming": ["Traversy Media", "freeCodeCamp", "Fireship", "The Coding Train"],
    "physics": ["Physics Girl", "minutephysics", "Physics Explained"],
    "chemistry": ["NileRed", "Periodic Videos", "The Chemistry Channel"],
    "biology": ["CrashCourse", "Khan Academy", "Amoeba Sisters"],
    "history": ["History Matters", "Oversimplified", "History Buffs"],
    "general": ["CrashCourse", "Khan Academy", "TED-Ed", "Vsauce"]
}

# Channel IDs (you can expand this list)
CHANNEL_IDS = {
    "3Blue1Brown": "UCYO_jab_esuFRV4b17AJtAw",
    "Khan Academy": "UC4a-Gbdw7vOaccHmFo40b9g",
    "CrashCourse": "UCX6b17PVsYBQ0ip5gyeme-Q",
    "freeCodeCamp": "UC8butISFwT-Wl7EV0hUK0BQ",
    "Kurzgesagt": "UCsXVk37bltHxD1rDPwtNM8Q",
    "Veritasium": "UCHnyfMqiRRG1u-2MsSQLbXA",
    "Vsauce": "UC6nSFpj9HTCZ5t-N3Rm3-HA"
}

def fetch_youtube_rss(query):
    """
    Fetches YouTube videos using public RSS feeds (no auth required).
    Strategy: Search YouTube's public RSS API.
    """
    results = []
    
    try:
        # Method 1: Use YouTube's search RSS (public, no auth)
        search_url = "https://www.youtube.com/results"
        params = {"search_query": query, "sp": "CAI%253D"}  # sp parameter for videos only
        
        # We'll get the search page and extract video IDs
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(search_url, params=params, headers=headers, timeout=5)
        
        if response.status_code == 200:
            # Extract video IDs from the HTML
            import re
            video_ids = re.findall(r'"videoId":"([^"]+)"', response.text)
            
            # Get unique video IDs (first 15)
            seen = set()
            unique_ids = []
            for vid_id in video_ids:
                if vid_id not in seen and len(unique_ids) < 15:
                    seen.add(vid_id)
                    unique_ids.append(vid_id)
            
            # Fetch details for each video using oembed (public API, no auth)
            for vid_id in unique_ids[:10]:
                try:
                    oembed_url = f"https://www.youtube.com/oembed"
                    oembed_params = {"url": f"https://www.youtube.com/watch?v={vid_id}", "format": "json"}
                    
                    oembed_response = requests.get(oembed_url, params=oembed_params, timeout=3)
                    
                    if oembed_response.status_code == 200:
                        video_data = oembed_response.json()
                        
                        results.append({
                            "title": video_data.get("title", "YouTube Video"),
                            "url": f"https://www.youtube.com/watch?v={vid_id}",
                            "type": "video",
                            "description": f"by {video_data.get('author_name', 'Unknown')}",
                            "source": "YouTube",
                            "duration": 600,  # Default estimate
                            "thumbnail": video_data.get("thumbnail_url", f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg"),
                            "views": 0
                        })
                        
                except Exception as e:
                    print(f"Error fetching video {vid_id}: {e}")
                    continue
            
            if results:
                print(f"YouTube RSS: Found {len(results)} videos")
                return results
                
    except Exception as e:
        print(f"YouTube RSS error: {e}")
    
    # Fallback: Return empty (Wikipedia will still provide content)
    print("YouTube RSS: No videos found")
    return []

def fetch_piped(query):
    """
    Wrapper to maintain compatibility - uses YouTube RSS feeds.
    """
    return fetch_youtube_rss(query)
