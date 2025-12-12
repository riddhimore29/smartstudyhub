
import math

# Keywords for analysis
CLARITY_KEYWORDS = ["easy", "simple", "beginner", "basics", "intro", "introduction", "summary", "explained", "tutorial"]
DEPTH_KEYWORDS = ["advanced", "deep dive", "complete guide", "full course", "comprehensive", "detailed", "thesis", "analysis", "study", "documentation"]

def calculate_score(query, resource, filter_type):
    """
    Calculates a score (0-100) based on strict relevance and filter-specific weights.
    Applies logic: Score = Relevance + Clarity + Depth + Time + Source
    """
    query_lower = query.lower()
    title = resource.get('title', '').lower()
    desc = resource.get('description', '').lower()
    res_type = resource.get('type', 'article').lower().strip()
    duration = resource.get('duration', 0)
    url = resource.get('url', '').lower()
    source = resource.get('source', '').lower()
    
    breakdown = {}
    
    # ---------------------------------------------------------
    # 1. RELEVANCE (Base 0-40)
    # ---------------------------------------------------------
    relevance_score = 0
    keywords = query_lower.split()
    matched_count = 0
    
    # Title Match (High Weight)
    if query_lower in title:
        relevance_score += 20
    else:
        for word in keywords:
            if len(word) < 3: continue
            if word in title:
                relevance_score += 10
                matched_count += 1
                
    # Desc Match (Low Weight)
    for word in keywords:
        if len(word) < 3: continue
        if word in desc:
            relevance_score += 2
            
    relevance_score = min(40, relevance_score)
    breakdown['relevance'] = relevance_score

    # ---------------------------------------------------------
    # 2. TIME FACTOR (Base 0-20) - MODE DEPENDENT
    # ---------------------------------------------------------
    time_score = 0
    minutes = duration / 60
    
    if filter_type == 'quick':
        # BONUS: Very Short (< 6m) -> +20
        # BONUS: Short (6-15m) -> +15
        # PENALTY: Long (> 20m) -> -20 (But filter should catch this)
        if res_type == 'video':
            if 0 < minutes <= 6: time_score = 20
            elif 6 < minutes <= 15: time_score = 15
            else: time_score = -20
        else: # Article
            # Estimate: Short articles good
            time_score = 10
            
    elif filter_type == 'deep':
        # BONUS: Long (> 20m) -> +20
        # PENALTY: Short (< 10m) -> -10
        if res_type == 'video':
            if minutes >= 20: time_score = 20
            elif 10 <= minutes < 20: time_score = 5
            elif minutes > 0 and minutes < 10: time_score = -10
        else: # Article/PDF
            if res_type == 'pdf': time_score = 20 # PDFs assumed deep
            else: time_score = 10 
            
    else: # ALL / VIDEO / ARTICLE
        # Neutral: Slight checking for "too short" or "too long" extremity?
        # Actually preference for "substantial" content (5-60 mins)
        if res_type == 'video':
            if minutes < 1: time_score = 0 # Shorts/TikToks less valuable for study?
            elif 5 <= minutes <= 60: time_score = 10
            else: time_score = 5
        else:
            time_score = 5

    breakdown['time'] = time_score

    # ---------------------------------------------------------
    # 3. DEPTH & CLARITY (Base 0-20)
    # ---------------------------------------------------------
    concept_score = 0
    
    has_clarity = any(k in title or k in desc for k in CLARITY_KEYWORDS)
    has_depth = any(k in title or k in desc for k in DEPTH_KEYWORDS)
    
    if filter_type == 'quick':
        if has_clarity: concept_score += 10
        if has_depth: concept_score -= 5 # "Complete course" is bad for quick
        
    elif filter_type == 'deep':
        if has_depth: concept_score += 20
        if has_clarity: concept_score += 5 # Good to be clear even if deep
        
    else:
        if has_clarity: concept_score += 5
        if has_depth: concept_score += 10

    breakdown['concept'] = concept_score

    # ---------------------------------------------------------
    # 4. SOURCE QUALITY (Base 0-10)
    # ---------------------------------------------------------
    quality_score = 5 # Neutral start
    
    if 'wikipedia' in source: quality_score = 8
    if '.edu' in url or '.gov' in url: quality_score = 10
    if 'pdf' in res_type: quality_score += 2
    
    breakdown['quality'] = min(10, quality_score)
    
    # ---------------------------------------------------------
    # 5. TYPE BIAS (Base 0-10) - Ensuring Mix in ALL
    # ---------------------------------------------------------
    type_score = 0
    if filter_type == 'all':
        if res_type == 'video': type_score = 5 # Users usually want videos
        if res_type == 'article': type_score = 3
    
    breakdown['type'] = type_score

    # ---------------------------------------------------------
    # FINAL SUM
    # ---------------------------------------------------------
    total = relevance_score + time_score + concept_score + quality_score + type_score
    return max(0, min(100, total)), breakdown


def rank_resources(query, resources, filter_type="all"):
    """
    Ranks resources using strict categorization and filtering rules.
    
    Modes:
    - all: Top 5 BEST (Video + Article + PDF scorable).
    - quick: Strictly SHORT content (<15m video, short articles).
    - deep: Strictly LONG content (>20m video, PDFs, long articles).
    - video: Strictly VIDEOS.
    - article: Strictly ARTICLES + PDFS (No videos).
    """
    filter_type = filter_type.lower()
    filtered_list = []
    
    print(f"\n--- RANKING START: {filter_type.upper()} ---")
    print(f"Total Raw Inputs: {len(resources)}")
    
    # DEBUG COUNTS
    c_vid = sum(1 for r in resources if r.get('type')=='video')
    c_art = sum(1 for r in resources if r.get('type')=='article')
    c_pdf = sum(1 for r in resources if r.get('type')=='pdf')
    print(f"Inputs: Videos={c_vid}, Articles={c_art}, PDFs={c_pdf}")

    for res in resources:
        # 1. NORMALIZE TYPE
        r_type = res.get('type', 'article').lower().strip()
        duration = res.get('duration', 0) # Seconds
        minutes = duration / 60
        
        keep = False
        
        # 2. FILTER LOGIC
        if filter_type == 'all':
            keep = True # Everything competes based on score
            
        elif filter_type == 'video':
            if r_type == 'video': keep = True
            
        elif filter_type == 'article':
            # Article tab includes PDF + Article, excludes Video
            if r_type in ['article', 'pdf']: keep = True
            
        elif filter_type == 'quick':
            # HARD FILTER: Short content only
            if r_type == 'video':
                if minutes <= 15: keep = True # Strict < 15 min
            else:
                # Assume articles are quick unless marked as huge PDF?
                # Actually, exclude PDFs in Quick usually, as they are heavy.
                if r_type == 'article': keep = True
                if r_type == 'pdf': keep = False # PDFs are rarely quick
                
        elif filter_type == 'deep':
            # HARD FILTER: Long content only
            if r_type == 'video':
                if minutes >= 20: keep = True # Strict > 20 min
            else:
                if r_type == 'pdf': keep = True
                if r_type == 'article': keep = True # We can't easily judge word count, allow them but ranker checks depth keywords
        
        if not keep:
            continue

        # 3. CALCULATE SCORE
        score, breakdown = calculate_score(query, res, filter_type)
        res['score'] = score
        res['why_selected'] = breakdown
        filtered_list.append(res)
        
    # 4. SORT BY SCORE DESCENDING
    filtered_list.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"Filtered Results: {len(filtered_list)}")
    if filtered_list:
        print(f"Top 1 Score: {filtered_list[0]['score']} ({filtered_list[0]['title']})")
    
    # 5. RETURN TOP 5
    return filtered_list[:5]
