import requests
from bs4 import BeautifulSoup
import urllib.parse

def test_ddg_videos(query):
    print(f"Testing DDG Video Search for: {query}")
    
    # DDG Video Search URL (scraping html.duckduckgo.com usually gives mixed, but we can try to find youtube links)
    # Alternatively, use the 'videos' tab params? html.duckduckgo doesn't support tabs well.
    # Let's try standard html search and look for youtube links.
    
    url = "https://html.duckduckgo.com/html/"
    data = {'q': query + " youtube"} # Force youtube results
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        found = 0
        for res in soup.find_all('div', class_='result'):
            a_tag = res.find('a', class_='result__a')
            if not a_tag: continue
            
            link = a_tag.get('href')
            link = urllib.parse.unquote(link)
            if "uddg=" in link:
                link = link.split("uddg=")[1].split("&")[0]
                
            if "youtube.com/watch" in link or "youtu.be" in link:
                print(f"FOUND VIDEO: {link}")
                print(f"  Title: {a_tag.get_text(strip=True)}")
                found += 1
                if found >= 5: break
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ddg_videos("binary search")
