from providers.piped import fetch_piped
from providers.duckduckgo import fetch_duckduckgo
from providers.wikipedia import fetch_wikipedia

# Query that failed
query = "Machine Learning"

print(f"--- Query: {query} ---")

print("\n[Piped/Invidious]")
try:
    videos = fetch_piped(query)
    print(f"Count: {len(videos)}")
    # print(videos[:2])
except Exception as e:
    print(f"Error: {e}")

print("\n[DuckDuckGo]")
try:
    # Test strict pdf search simulation
    docs = fetch_duckduckgo(query)
    pdfs = [d for d in docs if d['type'] == 'pdf']
    print(f"Total: {len(docs)}, PDFs: {len(pdfs)}")
except Exception as e:
    print(f"Error: {e}")
