"""Seed data — full hierarchical category taxonomy.

This is the single source of truth for the category tree.
Categories are upserted on app startup so the DB is always in sync.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

# Each entry: {slug, name, icon, color, description?, children?[]}
# Icons use Lucide icon names (used by shadcn/ui on the frontend).

CATEGORY_SEED: List[Dict[str, Any]] = [
    {
        "slug": "world",
        "name": "World",
        "icon": "globe",
        "color": "#3B82F6",
        "description": "International news and global affairs",
        "children": [
            {"slug": "world-conflicts", "name": "Conflicts & War", "icon": "swords", "color": "#EF4444"},
            {"slug": "world-diplomacy", "name": "Diplomacy", "icon": "handshake", "color": "#6366F1"},
            {"slug": "world-humanitarian", "name": "Humanitarian", "icon": "heart-handshake", "color": "#EC4899"},
        ],
    },
    {
        "slug": "politics",
        "name": "Politics & Government",
        "icon": "landmark",
        "color": "#8B5CF6",
        "description": "Government policy, elections, legislation",
        "children": [
            {"slug": "politics-elections", "name": "Elections", "icon": "vote", "color": "#7C3AED"},
            {"slug": "politics-policy", "name": "Policy & Regulation", "icon": "scale", "color": "#6D28D9"},
        ],
    },
    {
        "slug": "business",
        "name": "Business & Finance",
        "icon": "briefcase",
        "color": "#0EA5E9",
        "description": "Corporate news, markets, investing",
        "children": [
            {"slug": "business-markets", "name": "Markets & Stocks", "icon": "trending-up", "color": "#0284C7"},
            {"slug": "business-economy", "name": "Economy & Macro", "icon": "bar-chart-3", "color": "#0369A1"},
            {"slug": "business-startups", "name": "Startups & VC", "icon": "rocket", "color": "#06B6D4"},
            {"slug": "business-crypto", "name": "Crypto & Blockchain", "icon": "bitcoin", "color": "#F59E0B"},
        ],
    },
    {
        "slug": "technology",
        "name": "Technology",
        "icon": "cpu",
        "color": "#6366F1",
        "description": "Tech industry, software, hardware, internet",
        "children": [
            {"slug": "tech-ai", "name": "Artificial Intelligence", "icon": "brain", "color": "#8B5CF6"},
            {"slug": "tech-software", "name": "Software & Apps", "icon": "code", "color": "#7C3AED"},
            {"slug": "tech-hardware", "name": "Hardware & Gadgets", "icon": "smartphone", "color": "#6D28D9"},
            {"slug": "tech-cybersecurity", "name": "Cybersecurity", "icon": "shield", "color": "#DC2626"},
            {"slug": "tech-social-media", "name": "Social Media", "icon": "share-2", "color": "#2563EB"},
        ],
    },
    {
        "slug": "science",
        "name": "Science",
        "icon": "flask-conical",
        "color": "#14B8A6",
        "description": "Scientific discoveries, research, academia",
        "children": [
            {"slug": "science-space", "name": "Space & Astronomy", "icon": "telescope", "color": "#1E3A5F"},
            {"slug": "science-physics", "name": "Physics", "icon": "atom", "color": "#0D9488"},
            {"slug": "science-biology", "name": "Biology & Biotech", "icon": "dna", "color": "#059669"},
            {"slug": "science-earth", "name": "Earth Sciences", "icon": "mountain", "color": "#65A30D"},
        ],
    },
    {
        "slug": "health",
        "name": "Health & Medicine",
        "icon": "heart-pulse",
        "color": "#EF4444",
        "description": "Public health, medical research, healthcare industry",
        "children": [
            {"slug": "health-disease", "name": "Disease & Outbreaks", "icon": "virus", "color": "#DC2626"},
            {"slug": "health-pharma", "name": "Pharma & Biotech", "icon": "pill", "color": "#B91C1C"},
            {"slug": "health-wellness", "name": "Wellness & Fitness", "icon": "dumbbell", "color": "#F97316"},
            {"slug": "health-mental", "name": "Mental Health", "icon": "brain", "color": "#A855F7"},
        ],
    },
    {
        "slug": "environment",
        "name": "Environment & Climate",
        "icon": "leaf",
        "color": "#22C55E",
        "description": "Climate change, conservation, ecology",
        "children": [
            {"slug": "env-climate", "name": "Climate Change", "icon": "thermometer-sun", "color": "#EF4444"},
            {"slug": "env-conservation", "name": "Conservation", "icon": "trees", "color": "#16A34A"},
            {"slug": "env-pollution", "name": "Pollution", "icon": "factory", "color": "#78716C"},
        ],
    },
    {
        "slug": "energy",
        "name": "Energy & Sustainability",
        "icon": "zap",
        "color": "#F59E0B",
        "description": "Renewable energy, fossil fuels, energy policy, sustainable economy — SDG-aligned",
        "children": [
            {"slug": "energy-solar", "name": "Solar", "icon": "sun", "color": "#FBBF24"},
            {"slug": "energy-wind", "name": "Wind", "icon": "wind", "color": "#38BDF8"},
            {"slug": "energy-nuclear", "name": "Nuclear", "icon": "atom", "color": "#A3E635"},
            {"slug": "energy-oil-gas", "name": "Oil & Gas", "icon": "droplet", "color": "#78716C"},
            {"slug": "energy-ev", "name": "EVs & E-Mobility", "icon": "car", "color": "#10B981"},
            {"slug": "energy-policy", "name": "Energy Policy", "icon": "file-text", "color": "#6366F1"},
            {"slug": "energy-grid", "name": "Grid & Storage", "icon": "battery-charging", "color": "#14B8A6"},
        ],
    },
    {
        "slug": "education",
        "name": "Education",
        "icon": "graduation-cap",
        "color": "#2563EB",
        "description": "Schools, universities, online learning, education policy",
    },
    {
        "slug": "law",
        "name": "Law & Justice",
        "icon": "gavel",
        "color": "#78716C",
        "description": "Legal news, court rulings, justice system",
    },
    {
        "slug": "crime",
        "name": "Crime & Safety",
        "icon": "siren",
        "color": "#DC2626",
        "description": "Crime reports, public safety, policing",
    },
    {
        "slug": "sports",
        "name": "Sports",
        "icon": "trophy",
        "color": "#F97316",
        "description": "Professional and amateur sports worldwide",
        "children": [
            {"slug": "sports-football", "name": "Football / Soccer", "icon": "circle-dot", "color": "#16A34A"},
            {"slug": "sports-basketball", "name": "Basketball", "icon": "circle", "color": "#EA580C"},
            {"slug": "sports-tennis", "name": "Tennis", "icon": "circle-dot", "color": "#FBBF24"},
            {"slug": "sports-motorsport", "name": "Motorsport", "icon": "car", "color": "#EF4444"},
            {"slug": "sports-olympics", "name": "Olympics", "icon": "medal", "color": "#D4AF37"},
            {"slug": "sports-esports", "name": "Esports", "icon": "gamepad-2", "color": "#8B5CF6"},
        ],
    },
    {
        "slug": "entertainment",
        "name": "Entertainment",
        "icon": "clapperboard",
        "color": "#EC4899",
        "description": "Movies, TV, music, celebrity, pop culture",
        "children": [
            {"slug": "entertainment-movies", "name": "Movies & TV", "icon": "tv", "color": "#DB2777"},
            {"slug": "entertainment-music", "name": "Music", "icon": "music", "color": "#C026D3"},
            {"slug": "entertainment-celebrity", "name": "Celebrity", "icon": "star", "color": "#F59E0B"},
            {"slug": "entertainment-gaming", "name": "Gaming", "icon": "gamepad-2", "color": "#7C3AED"},
        ],
    },
    {
        "slug": "arts-culture",
        "name": "Arts & Culture",
        "icon": "palette",
        "color": "#A855F7",
        "description": "Fine arts, literature, theatre, cultural heritage",
    },
    {
        "slug": "lifestyle",
        "name": "Lifestyle",
        "icon": "sparkles",
        "color": "#F472B6",
        "description": "Fashion, food, travel, relationships, home",
        "children": [
            {"slug": "lifestyle-food", "name": "Food & Drink", "icon": "utensils", "color": "#FB923C"},
            {"slug": "lifestyle-travel", "name": "Travel", "icon": "plane", "color": "#38BDF8"},
            {"slug": "lifestyle-fashion", "name": "Fashion", "icon": "shirt", "color": "#E879F9"},
            {"slug": "lifestyle-home", "name": "Home & Garden", "icon": "home", "color": "#4ADE80"},
        ],
    },
    {
        "slug": "automotive",
        "name": "Automotive",
        "icon": "car",
        "color": "#64748B",
        "description": "Cars, trucks, automotive industry, reviews",
    },
    {
        "slug": "real-estate",
        "name": "Real Estate",
        "icon": "building",
        "color": "#0D9488",
        "description": "Property markets, housing, commercial real estate",
    },
    {
        "slug": "religion",
        "name": "Religion & Faith",
        "icon": "church",
        "color": "#92400E",
        "description": "Religious news, interfaith dialogue, spirituality",
    },
    {
        "slug": "opinion",
        "name": "Opinion & Editorial",
        "icon": "message-square",
        "color": "#475569",
        "description": "Op-eds, columns, analysis, commentary",
    },
    {
        "slug": "local",
        "name": "Local & Regional",
        "icon": "map-pin",
        "color": "#059669",
        "description": "Local and regional news by geography",
    },
    {
        "slug": "breaking",
        "name": "Breaking News",
        "icon": "alert-triangle",
        "color": "#EF4444",
        "description": "Urgent, just-in stories across all categories",
    },
]
