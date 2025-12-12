import requests
from bs4 import BeautifulSoup
import urllib.parse

# Curated programming tutorial links for common topics
CURATED_TUTORIALS = {
    "python": [
        {"title": "Python Tutorial", "url": "https://www.w3schools.com/python/", "source": "W3Schools"},
        {"title": "Python Programming", "url": "https://www.geeksforgeeks.org/python-programming-language/", "source": "GeeksforGeeks"},
        {"title": "Learn Python", "url": "https://www.tutorialspoint.com/python/index.htm", "source": "TutorialsPoint"},
        {"title": "Python Guide", "url": "https://www.javatpoint.com/python-tutorial", "source": "JavaTpoint"},
    ],
    "javascript": [
        {"title": "JavaScript Tutorial", "url": "https://www.w3schools.com/js/", "source": "W3Schools"},
        {"title": "JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "source": "MDN Web Docs"},
        {"title": "JavaScript Programming", "url": "https://www.geeksforgeeks.org/javascript/", "source": "GeeksforGeeks"},
        {"title": "Learn JavaScript", "url": "https://www.tutorialspoint.com/javascript/index.htm", "source": "TutorialsPoint"},
    ],
    "java": [
        {"title": "Java Tutorial", "url": "https://www.w3schools.com/java/", "source": "W3Schools"},
        {"title": "Java Programming", "url": "https://www.geeksforgeeks.org/java/", "source": "GeeksforGeeks"},
        {"title": "Learn Java", "url": "https://www.javatpoint.com/java-tutorial", "source": "JavaTpoint"},
    ],
    "c++": [
        {"title": "C++ Tutorial", "url": "https://www.w3schools.com/cpp/", "source": "W3Schools"},
        {"title": "C++ Programming", "url": "https://www.geeksforgeeks.org/c-plus-plus/", "source": "GeeksforGeeks"},
        {"title": "Learn C++", "url": "https://www.tutorialspoint.com/cplusplus/index.htm", "source": "TutorialsPoint"},
    ],
    "html": [
        {"title": "HTML Tutorial", "url": "https://www.w3schools.com/html/", "source": "W3Schools"},
        {"title": "HTML Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/HTML", "source": "MDN Web Docs"},
        {"title": "Learn HTML", "url": "https://www.geeksforgeeks.org/html-tutorial/", "source": "GeeksforGeeks"},
    ],
    "css": [
        {"title": "CSS Tutorial", "url": "https://www.w3schools.com/css/", "source": "W3Schools"},
        {"title": "CSS Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/CSS", "source": "MDN Web Docs"},
        {"title": "Learn CSS", "url": "https://www.geeksforgeeks.org/css-tutorial/", "source": "GeeksforGeeks"},
    ],
    "react": [
        {"title": "React Tutorial", "url": "https://www.w3schools.com/react/", "source": "W3Schools"},
        {"title": "React Docs", "url": "https://react.dev/learn", "source": "React Official"},
        {"title": "Learn React", "url": "https://www.geeksforgeeks.org/react-tutorial/", "source": "GeeksforGeeks"},
    ],
    "sql": [
        {"title": "SQL Tutorial", "url": "https://www.w3schools.com/sql/", "source": "W3Schools"},
        {"title": "SQL Programming", "url": "https://www.geeksforgeeks.org/sql-tutorial/", "source": "GeeksforGeeks"},
        {"title": "Learn SQL", "url": "https://www.tutorialspoint.com/sql/index.htm", "source": "TutorialsPoint"},
    ],
    "data structures": [
        {"title": "Data Structures Tutorial", "url": "https://www.geeksforgeeks.org/data-structures/", "source": "GeeksforGeeks"},
        {"title": "Learn Data Structures", "url": "https://www.tutorialspoint.com/data_structures_algorithms/index.htm", "source": "TutorialsPoint"},
        {"title": "DS Guide", "url": "https://www.javatpoint.com/data-structure-tutorial", "source": "JavaTpoint"},
    ],
    "algorithms": [
        {"title": "Algorithms Tutorial", "url": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/", "source": "GeeksforGeeks"},
        {"title": "Learn Algorithms", "url": "https://www.tutorialspoint.com/data_structures_algorithms/algorithms_basics.htm", "source": "TutorialsPoint"},
    ],
    "machine learning": [
        {"title": "Machine Learning Tutorial", "url": "https://www.geeksforgeeks.org/machine-learning/", "source": "GeeksforGeeks"},
        {"title": "ML with Python", "url": "https://www.tutorialspoint.com/machine_learning_with_python/index.htm", "source": "TutorialsPoint"},
        {"title": "Learn ML", "url": "https://www.javatpoint.com/machine-learning", "source": "JavaTpoint"},
    ]
}

def get_curated_tutorials(query):
    """
    Returns curated tutorial links for common programming topics.
    """
    query_lower = query.lower().strip()
    results = []
    
    # Check for exact or partial matches
    for topic, tutorials in CURATED_TUTORIALS.items():
        if topic in query_lower or query_lower in topic:
            for tut in tutorials:
                results.append({
                    "title": tut["title"],
                    "url": tut["url"],
                    "type": "article",
                    "description": f"Comprehensive tutorial from {tut['source']}",
                    "source": tut["source"],
                    "duration": 0
                })
    
    return results

def fetch_duckduckgo(query):
    """
    Provides curated programming tutorial links for common topics.
    """
    results = []
    
    # Get curated tutorials
    curated = get_curated_tutorials(query)
    if curated:
        results.extend(curated)
        print(f"Web search: Found {len(results)} curated programming tutorials")
    else:
        print("Web search: No curated tutorials for this topic (Wikipedia still provides results)")
    
    return results
