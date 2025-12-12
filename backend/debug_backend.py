import concurrent.futures
import pprint
from providers.piped import fetch_piped
from providers.duckduckgo import fetch_duckduckgo
from providers.wikipedia import fetch_wikipedia
from ranking import rank_resources

QUERIES = ["binary search"]

def debug_query(query):
    print(f"\n{'='*20} TESTING QUERY: '{query}' {'='*20}")
    
    # 1. Fetch
    print("\n--- Fetching ---")
    
    wiki_res = []
    ddg_res = []
    piped_res = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f_wiki = executor.submit(fetch_wikipedia, query)
        f_ddg = executor.submit(fetch_duckduckgo, query)
        f_piped = executor.submit(fetch_piped, query)
        
        try:
            wiki_res = f_wiki.result()
            print(f"Wiki found: {len(wiki_res)}")
            if wiki_res: print(f"  Top Wiki: {wiki_res[0]['title']}")
        except Exception as e: print(f"Wiki Failed: {e}")

        try:
            ddg_res = f_ddg.result()
            print(f"DDG found: {len(ddg_res)}")
            if ddg_res: print(f"  Top DDG: {ddg_res[0]['title']}")
        except Exception as e: print(f"DDG Failed: {e}")

        try:
            piped_res = f_piped.result()
            print(f"Piped found: {len(piped_res)}")
            if piped_res: print(f"  Top Piped: {piped_res[0]['title']} ({piped_res[0]['duration']}s)")
        except Exception as e: print(f"Piped Failed: {e}")

    # 2. Merge
    all_res = wiki_res + ddg_res + piped_res
    print(f"\nTotal Raw Items: {len(all_res)}")
    
    # 3. Rank
    print("\n--- Ranking (Top 5) ---")
    ranked = rank_resources(query, all_res, "all")
    
    for i, item in enumerate(ranked, 1):
        print(f"{i}. [{item['type'].upper()}] {item['title']} (Score: {item.get('score')})")
        print(f"   Source: {item['source']}")
        print(f"   Breakdown: {item.get('why_selected', {})}")

if __name__ == "__main__":
    for q in QUERIES:
        debug_query(q)
