# SmartStudyHub

A beautiful, modern web application that aggregates and ranks expert study materials from across the web.

## 🚀 Features

- **Multi-Source Search**: Live results from YouTube (Piped), DuckDuckGo, and Wikipedia.
- **Smart Ranking**: Custom algorithm ranks content by relevance, clarity, depth, and quality.
- **Intelligent Formatting**: 
  - ⚡ **Quick**: Filters for short videos and summaries.
  - 🧠 **Deep**: Prioritizes comprehensive guides and long-form content.
- **Privacy Focused**: No login required, no tracking.
- **Modern UI**: Fully responsive, animated, and clean interface.

## 🛠️ Tech Stack

- **Frontend**: HTML5, TailwindCSS (CDN), Vanilla JavaScript.
- **Backend**: Python Flask.
- **APIs**: Piped (YouTube), DuckDuckGo, Wikipedia.

## 📦 Installation & Run Instructions

### Prerequisites
- Python 3.8+ installed.

### 1. Backend Setup

1. Open a terminal in the project folder:
   ```bash
   cd study_resource_finder
   ```

2. Install dependencies:
   ```bash
   pip install flask flask-cors requests
   ```

3. Run the backend server:
   ```bash
   python backend/app.py
   ```
   *The server will start at `http://127.0.0.1:5000`.*

### 2. Frontend Setup

1. Go to the `study_resource_finder/frontend` folder.
2. Open `index.html` in your browser (Chrome/Edge/Firefox).
   - You can simply double-click the file, or use a live server extension.

### 3. Usage

1. Enter a topic (e.g., "Binary Search" or "Photosynthesis") on the landing page.
2. Click **Search**.
3. View the top ranked results.
4. Use the filter chips (Quick, Deep, Video, etc.) to refine your results.
5. Click "Why recommended?" to see the transparent scoring breakdown.

## 📂 Project Structure

```
study_resource_finder/
├── backend/
│   ├── app.py              # Main Flask App
│   ├── ranking.py          # Scoring Algorithm
│   └── providers/          # API Integrations
│       ├── piped.py
│       ├── duckduckgo.py
│       └── wikipedia.py
└── frontend/
    ├── index.html          # Landing Page
    ├── search.html         # Results Page
    └── assets/
        ├── style.css       # Custom Styles
        └── script.js       # Frontend Logic
```

## ✨ Credits

Built as a demonstration of advanced agentic coding capabilities.
