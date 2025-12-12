const API_BASE = "/api/search";

// State
let currentQuery = new URLSearchParams(window.location.search).get('q');
let currentFilter = 'all';

// Init
document.addEventListener('DOMContentLoaded', () => {
    if (currentQuery) {
        document.getElementById('query-display').textContent = currentQuery;
        document.getElementById('search-input').value = currentQuery;
        fetchResources(currentQuery, currentFilter);
    } else {
        // If on search page without query, redirect to home or show blank
        if (window.location.pathname.includes('search.html') && !currentQuery) {
            window.location.href = '/';
        }
    }

    // Enter key support
    const searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.target.value.trim()) {
                window.location.href = `search.html?q=${encodeURIComponent(e.target.value.trim())}`;
            }
        });
    }
});

// Landing Page Search
function performSearch() {
    const query = document.getElementById('landing-search').value.trim();
    if (query) {
        window.location.href = `search.html?q=${encodeURIComponent(query)}`;
    }
}

function quickSearch(query) {
    window.location.href = `search.html?q=${encodeURIComponent(query)}`;
}

// Filter Handler
function setFilter(filterType) {
    currentFilter = filterType;

    // Update active state
    document.querySelectorAll('.pill-btn').forEach(btn => {
        // Reset to default
        btn.className = "pill-btn px-4 py-1.5 rounded-full text-xs font-semibold text-slate-600 bg-white border border-slate-200 hover:border-indigo-300 transition-all cursor-pointer";

        // Match?
        if (btn.getAttribute('onclick').includes(`'${filterType}'`)) {
            btn.className = "pill-btn active px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wide border border-transparent text-indigo-700 bg-white shadow-sm ring-1 ring-indigo-100 transition-all cursor-pointer";
        }
    });

    fetchResources(currentQuery, currentFilter);
}

// Fetch Logic
async function fetchResources(query, filter) {
    const container = document.getElementById('results-container');
    const loader = document.getElementById('loader');
    const errorState = document.getElementById('error-state');

    if (!container) return; // Guard clause

    // Show loading
    container.innerHTML = '';
    container.appendChild(loader);
    if (errorState) container.appendChild(errorState);
    loader.classList.remove('hidden');
    if (errorState) errorState.classList.add('hidden');

    try {
        const res = await fetch(`${API_BASE}?q=${encodeURIComponent(query)}&filter=${filter}`);
        const data = await res.json();

        loader.classList.add('hidden');

        if (!data.results || data.results.length === 0) {
            if (errorState) errorState.classList.remove('hidden');
            return;
        }

        // Render Items
        data.results.forEach((item, index) => {
            container.appendChild(createResponsiveCard(item, index));
        });

    } catch (err) {
        console.error(err);
        loader.classList.add('hidden');
        if (errorState) {
            errorState.classList.remove('hidden');
            errorState.querySelector('h3').textContent = "Connection Failed";
        }
    }
}

// PREMIUM CARD GENERATOR (Dark Mode)
function createResponsiveCard(item, index) {
    const isVideo = item.type === 'video';
    const card = document.createElement('div');

    // Animation Delay
    card.style.animationDelay = `${index * 0.1}s`;
    card.className = "glass-card rounded-2xl p-0 relative fade-in-up hover:z-10 overflow-hidden flex flex-col md:flex-row group border border-white/5 bg-slate-900/40";

    // Score Badge
    const scoreColor = item.score > 80 ? 'text-emerald-400 bg-emerald-900/30 border-emerald-500/30' :
        (item.score > 50 ? 'text-indigo-400 bg-indigo-900/30 border-indigo-500/30' : 'text-amber-400 bg-amber-900/30 border-amber-500/30');

    const scoreBadge = `
        <div class="absolute top-4 right-4 z-20 flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold ${scoreColor} border shadow-sm backdrop-blur-md">
            <i class="fa-solid fa-star text-[10px]"></i> ${item.score}
        </div>
    `;

    if (isVideo) {
        // --- VIDEO CARD LAYOUT ---
        const thumbUrl = item.thumbnail || `https://via.placeholder.com/640x360.png?text=No+Thumbnail`;

        card.innerHTML = `
            ${scoreBadge}
            <!-- Thumbnail Section -->
            <div class="w-full md:w-1/3 relative aspect-video md:aspect-auto overflow-hidden bg-black group-cursor-pointer">
                 <a href="${item.url}" target="_blank" class="block h-full">
                    <img src="${thumbUrl}" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-105 transition duration-700" alt="${item.title}">
                    
                    <!-- Play Overlay -->
                    <div class="absolute inset-0 flex items-center justify-center">
                        <div class="w-12 h-12 bg-white/10 backdrop-blur-sm rounded-full flex items-center justify-center text-white border border-white/20 group-hover:scale-110 transition duration-300 shadow-lg">
                            <i class="fa-solid fa-play pl-1"></i>
                        </div>
                    </div>
                    
                    <!-- Duration Badge -->
                    <div class="absolute bottom-2 right-2 px-2 py-0.5 bg-black/80 backdrop-blur-sm rounded text-white text-[10px] font-bold tracking-wide border border-white/10">
                        ${formatDuration(item.duration)}
                    </div>
                </a>
            </div>

            <!-- Content Section -->
            <div class="flex-1 p-5 md:p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center gap-2 mb-2">
                        <span class="px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 text-[10px] font-bold uppercase tracking-wider border border-red-500/20">
                            Video
                        </span>
                        <span class="text-slate-500 text-xs">•</span>
                        <span class="text-slate-400 text-xs font-medium">${item.source}</span>
                    </div>

                    <a href="${item.url}" target="_blank" class="group/link">
                        <h3 class="text-base font-bold text-white group-hover/link:text-indigo-400 transition mb-2 line-clamp-2 leading-tight">
                            ${item.title}
                        </h3>
                    </a>

                    <p class="text-slate-400 text-sm mb-3 line-clamp-2 leading-relaxed">
                        ${item.description}
                    </p>

                    <!-- Why This Result? -->
                    ${generateWhyBadges(item.why_selected)}
                </div>

                <div class="flex items-center gap-3 text-xs text-slate-500">
                    <span class="flex items-center gap-1">
                        <i class="fa-solid fa-eye text-slate-600"></i> ${formatViews(item.views)}
                    </span>
                     <span class="flex items-center gap-1.5 ml-auto text-indigo-400 group-hover:translate-x-1 transition cursor-pointer">
                        Watch Now <i class="fa-solid fa-arrow-right"></i>
                     </span>
                </div>
            </div>
        `;
    } else {
        // --- ARTICLE / PDF CARD LAYOUT ---
        const isPdf = item.type === 'pdf';
        const iconClass = isPdf ? 'fa-file-pdf text-orange-400' : 'fa-newspaper text-blue-400';
        const bgClass = isPdf ? 'bg-orange-500/10 border-orange-500/20' : 'bg-blue-500/10 border-blue-500/20';
        const typeLabel = isPdf ? 'PDF Document' : 'Article';

        card.innerHTML = `
            ${scoreBadge}
            <div class="p-6 md:p-7 w-full flex flex-col h-full bg-gradient-to-br from-slate-900/50 to-black/50">
                <div class="flex items-start gap-4 mb-3">
                    <div class="w-12 h-12 rounded-2xl ${bgClass} flex items-center justify-center shrink-0 border border-white/5 shadow-sm">
                        <i class="fa-solid ${iconClass} text-xl"></i>
                    </div>
                    <div>
                         <div class="flex items-center gap-2 mb-1">
                            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500">${typeLabel}</span>
                            <span class="w-1 h-1 rounded-full bg-slate-700"></span>
                            <span class="text-[10px] font-semibold text-slate-600 truncate max-w-[150px]">${item.source}</span>
                        </div>
                        <a href="${item.url}" target="_blank">
                            <h3 class="text-lg font-bold text-slate-200 leading-tight group-hover:text-indigo-400 transition line-clamp-2">
                                ${item.title}
                            </h3>
                        </a>
                    </div>
                </div>

                <p class="text-sm text-slate-400 leading-relaxed line-clamp-3 mb-5 pl-[4rem]">
                    ${item.description || "Click to read more about this topic."}
                </p>

                <div class="mt-auto pl-[4rem] flex items-center gap-4">
                     <a href="${item.url}" target="_blank" class="inline-flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-indigo-400 transition group/btn">
                        Read this resource 
                        <span class="w-5 h-5 rounded-full bg-white/5 flex items-center justify-center group-hover/btn:translate-x-1 transition">
                            <i class="fa-solid fa-chevron-right text-[10px] text-indigo-400"></i>
                        </span>
                    </a>
                </div>
            </div>
        `;
    }

    return card;
}

// Helpers
function formatDuration(seconds) {
    if (!seconds) return "00:00";
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m}:${s.toString().padStart(2, '0')}`;
}

function formatViews(views) {
    if (!views) return "Popular";
    if (views >= 1000000) return (views / 1000000).toFixed(1) + 'M';
    if (views >= 1000) return (views / 1000).toFixed(1) + 'k';
    return views;
}
// Format duration in MM:SS
function formatDuration(s) {
    if (!s || s === 0) return '?';
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, '0')}`;
}

function formatViews(views) {
    if (!views) return "Popular";
    if (views >= 1000000) return (views / 1000000).toFixed(1) + 'M';
    if (views >= 1000) return (views / 1000).toFixed(1) + 'k';
    return views;
}

// Generate "Why this result?" badges
function generateWhyBadges(whySelected) {
    if (!whySelected) return '';

    const badges = [];

    if (whySelected.relevance >= 18) {
        badges.push('<span class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-indigo-500/10 text-indigo-300 text-[10px] font-semibold border border-indigo-500/20"><i class="fa-solid fa-bullseye"></i> Highly Relevant</span>');
    }

    if (whySelected.quality >= 7) {
        badges.push('<span class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-emerald-500/10 text-emerald-300 text-[10px] font-semibold border border-emerald-500/20"><i class="fa-solid fa-shield-halved"></i> Trusted Source</span>');
    }

    if (whySelected.time >= 15) {
        badges.push('<span class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-amber-500/10 text-amber-300 text-[10px] font-semibold border border-amber-500/20"><i class="fa-solid fa-clock"></i> Perfect Length</span>');
    }

    if (whySelected.concept >= 15) {
        badges.push('<span class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-purple-500/10 text-purple-300 text-[10px] font-semibold border border-purple-500/20"><i class="fa-solid fa-graduation-cap"></i> Beginner-Friendly</span>');
    } else if (whySelected.concept >= 10) {
        badges.push('<span class="inline-flex items-center gap-1 px-2 py-1 rounded-md bg-purple-500/10 text-purple-300 text-[10px] font-semibold border border-purple-500/20"><i class="fa-solid fa-brain"></i> Comprehensive</span>');
    }

    if (badges.length === 0) return '';

    return '<div class="flex flex-wrap gap-1.5 mt-3 pt-3 border-t border-white/5"><span class="text-[10px] text-slate-500 font-medium mr-1">Why picked:</span>' + badges.join('') + '</div>';
}
