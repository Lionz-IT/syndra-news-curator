"""Mock/seed article data — used when API keys are missing.

Generates realistic articles across ALL categories so the app always runs.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from typing import List

from app.schemas.article import ArticleCreate
from app.services.adapters import SourceAdapter

# ── Realistic seed data across all domains ────────────────
_MOCK_ARTICLES_DATA = [
    # World
    {
        "title": "G7 Leaders Announce Joint Climate-Security Pact at Summit",
        "body": "The Group of Seven nations unveiled a new framework linking climate resilience to national security, pledging $50 billion in combined funding over the next decade. The agreement emphasizes vulnerable coastal regions and small island states.",
        "source": "mock-newsapi",
        "url": "https://example.com/g7-climate-security",
        "author": "Sarah Chen",
        "category_slugs": ["world", "world-diplomacy", "environment"],
        "language": "en",
        "region": "global",
        "raw_tags": ["G7", "climate", "security", "diplomacy"],
    },
    {
        "title": "UN General Assembly Votes on New Digital Rights Resolution",
        "body": "A landmark resolution on digital rights and AI governance passed with 156 votes in favor. The resolution establishes principles for responsible AI deployment and data privacy protections across member states.",
        "source": "mock-guardian",
        "url": "https://example.com/un-digital-rights",
        "author": "James Wright",
        "category_slugs": ["world", "politics", "tech-ai"],
        "language": "en",
        "region": "global",
        "raw_tags": ["UN", "digital rights", "AI governance"],
    },
    # Politics
    {
        "title": "New Infrastructure Bill Passes Senate with Bipartisan Support",
        "body": "The $1.2 trillion infrastructure package cleared the Senate 69-30, allocating funds for roads, bridges, broadband internet, and electric vehicle charging networks. The bill now heads to conference committee.",
        "source": "mock-newsapi",
        "url": "https://example.com/infrastructure-bill",
        "author": "Michael Torres",
        "category_slugs": ["politics", "politics-policy"],
        "language": "en",
        "region": "north-america",
        "raw_tags": ["infrastructure", "senate", "legislation"],
    },
    # Business & Finance
    {
        "title": "Global Markets Rally as Central Banks Signal Rate Pause",
        "body": "Stock markets worldwide surged after the Federal Reserve, ECB, and Bank of Japan simultaneously signaled a pause in interest rate hikes. The S&P 500 gained 2.3% while European indices rose 1.8%.",
        "source": "mock-gnews",
        "url": "https://example.com/markets-rally-rates",
        "author": "Emily Rodriguez",
        "category_slugs": ["business", "business-markets"],
        "language": "en",
        "region": "global",
        "raw_tags": ["markets", "federal reserve", "interest rates"],
    },
    {
        "title": "Tech Startup Raises $500M to Build AI-Powered Supply Chain Platform",
        "body": "LogiMind, a San Francisco-based startup, secured a $500 million Series C round led by Sequoia Capital. The platform uses machine learning to optimize global supply chains and reduce waste by up to 40%.",
        "source": "mock-newsapi",
        "url": "https://example.com/logimind-funding",
        "author": "David Park",
        "category_slugs": ["business", "business-startups", "tech-ai"],
        "language": "en",
        "region": "north-america",
        "raw_tags": ["startup", "funding", "AI", "supply chain"],
    },
    # Technology
    {
        "title": "Major Breakthrough in Quantum Error Correction Achieved",
        "body": "Researchers at MIT demonstrated a new quantum error correction protocol that reduces qubit errors by 99.9%, bringing practical quantum computing significantly closer to reality.",
        "source": "mock-guardian",
        "url": "https://example.com/quantum-error-correction",
        "author": "Dr. Lisa Wang",
        "category_slugs": ["technology", "science"],
        "language": "en",
        "region": "north-america",
        "raw_tags": ["quantum computing", "research", "MIT"],
    },
    {
        "title": "EU Passes Comprehensive AI Regulation Framework",
        "body": "The European Parliament approved the AI Act with a decisive majority, establishing the world's first comprehensive legal framework for artificial intelligence. High-risk AI systems will face strict requirements.",
        "source": "mock-gnews",
        "url": "https://example.com/eu-ai-act",
        "author": "Anna Mueller",
        "category_slugs": ["technology", "tech-ai", "politics-policy"],
        "language": "en",
        "region": "europe",
        "raw_tags": ["EU", "AI regulation", "AI Act"],
    },
    # Science
    {
        "title": "James Webb Telescope Discovers New Earth-Like Exoplanet",
        "body": "NASA's James Webb Space Telescope has identified a rocky exoplanet in the habitable zone of a nearby star system, with atmospheric signatures suggesting the presence of water vapor.",
        "source": "mock-rss",
        "url": "https://example.com/jwst-exoplanet",
        "author": "Dr. Robert Chang",
        "category_slugs": ["science", "science-space"],
        "language": "en",
        "region": "global",
        "raw_tags": ["NASA", "JWST", "exoplanet", "space"],
    },
    # Health
    {
        "title": "WHO Approves New Malaria Vaccine for Children Under 5",
        "body": "The World Health Organization endorsed a second malaria vaccine, R21/Matrix-M, for use in children aged 5 months to 3 years. The vaccine showed 75% efficacy in clinical trials across four African countries.",
        "source": "mock-newsapi",
        "url": "https://example.com/who-malaria-vaccine",
        "author": "Grace Okafor",
        "category_slugs": ["health", "health-disease", "world"],
        "language": "en",
        "region": "africa",
        "raw_tags": ["WHO", "malaria", "vaccine", "public health"],
    },
    # Environment & Climate
    {
        "title": "Amazon Deforestation Drops 40% Under New Conservation Policy",
        "body": "Brazil reported a 40% reduction in Amazon deforestation over the past year, attributed to strengthened enforcement, indigenous land protections, and satellite monitoring systems.",
        "source": "mock-guardian",
        "url": "https://example.com/amazon-deforestation-drop",
        "author": "Carlos Silva",
        "category_slugs": ["environment", "env-conservation"],
        "language": "en",
        "region": "south-america",
        "raw_tags": ["Amazon", "deforestation", "Brazil", "conservation"],
    },
    # Energy & Sustainability (SDG-relevant)
    {
        "title": "World's Largest Offshore Wind Farm Begins Operation in North Sea",
        "body": "The 3.6 GW Dogger Bank Wind Farm started generating power, capable of supplying electricity to 6 million homes. The project represents a major milestone in the UK's net-zero strategy.",
        "source": "mock-rss",
        "url": "https://example.com/dogger-bank-wind",
        "author": "Tom Baker",
        "category_slugs": ["energy", "energy-wind"],
        "language": "en",
        "region": "europe",
        "raw_tags": ["wind energy", "offshore", "UK", "net zero"],
    },
    {
        "title": "Solar Panel Costs Hit Record Low, Now Cheaper Than Coal in 90% of World",
        "body": "The International Renewable Energy Agency reports that utility-scale solar PV costs have fallen below coal-fired generation in most markets, with prices reaching $0.028/kWh in competitive auctions.",
        "source": "mock-rss",
        "url": "https://example.com/solar-cost-record-low",
        "author": "Dr. Amara Osei",
        "category_slugs": ["energy", "energy-solar", "business-economy"],
        "language": "en",
        "region": "global",
        "raw_tags": ["solar", "IRENA", "energy costs", "renewable"],
    },
    {
        "title": "India Launches $20B Green Hydrogen Mission",
        "body": "India's cabinet approved a national green hydrogen mission targeting 5 million tonnes of annual production by 2030, with $20 billion in public-private investment to build electrolyzers and distribution infrastructure.",
        "source": "mock-newsapi",
        "url": "https://example.com/india-green-hydrogen",
        "author": "Priya Sharma",
        "category_slugs": ["energy", "energy-policy", "politics-policy"],
        "language": "en",
        "region": "asia",
        "raw_tags": ["India", "green hydrogen", "energy policy"],
    },
    # Sports
    {
        "title": "Champions League Final: Historic Comeback Stuns Favorites",
        "body": "In a dramatic Champions League final, the underdog side scored three goals in the last 20 minutes to overturn a 2-0 deficit, winning 3-2 in one of the most remarkable comebacks in tournament history.",
        "source": "mock-gnews",
        "url": "https://example.com/ucl-final-comeback",
        "author": "Marco Rossi",
        "category_slugs": ["sports", "sports-football"],
        "language": "en",
        "region": "europe",
        "raw_tags": ["Champions League", "football", "UEFA"],
    },
    # Entertainment
    {
        "title": "Award-Winning Director's New Film Breaks Box Office Records",
        "body": "The latest sci-fi epic from acclaimed director earned $250 million globally in its opening weekend, setting new records for the genre and earning critical praise for its visual effects.",
        "source": "mock-gnews",
        "url": "https://example.com/box-office-record",
        "author": "Jessica Kim",
        "category_slugs": ["entertainment", "entertainment-movies"],
        "language": "en",
        "region": "global",
        "raw_tags": ["movies", "box office", "sci-fi"],
    },
    # Education
    {
        "title": "Major Universities Adopt AI Tutoring Systems for STEM Courses",
        "body": "A consortium of 50 universities announced the adoption of AI-powered tutoring platforms for introductory STEM courses, reporting a 30% improvement in student pass rates during pilot programs.",
        "source": "mock-guardian",
        "url": "https://example.com/ai-tutoring-universities",
        "author": "Prof. Maria Gonzalez",
        "category_slugs": ["education", "tech-ai"],
        "language": "en",
        "region": "north-america",
        "raw_tags": ["education", "AI", "universities", "STEM"],
    },
    # Automotive
    {
        "title": "Electric Vehicle Sales Surpass Combustion Engine Cars in Norway",
        "body": "Norway became the first country where EVs outsold internal combustion engine vehicles for an entire year, with electric models accounting for 82% of all new car registrations.",
        "source": "mock-newsapi",
        "url": "https://example.com/norway-ev-sales",
        "author": "Erik Johansson",
        "category_slugs": ["automotive", "energy-ev"],
        "language": "en",
        "region": "europe",
        "raw_tags": ["EV", "Norway", "electric vehicles", "automotive"],
    },
    # Breaking News
    {
        "title": "Magnitude 7.2 Earthquake Strikes Near Pacific Coast",
        "body": "A powerful earthquake struck off the Pacific coast early this morning, triggering tsunami warnings for coastal areas. Emergency services are responding and initial reports indicate moderate damage.",
        "source": "mock-gnews",
        "url": "https://example.com/earthquake-pacific",
        "author": "Reuters Wire",
        "category_slugs": ["breaking", "world"],
        "language": "en",
        "region": "asia-pacific",
        "raw_tags": ["earthquake", "tsunami warning", "breaking"],
    },
    # Lifestyle
    {
        "title": "Plant-Based Cuisine Takes Center Stage at World's Top Restaurants",
        "body": "The latest Michelin Guide features a record number of plant-based restaurants, reflecting a global shift toward sustainable dining. Five new vegan-focused establishments received stars.",
        "source": "mock-guardian",
        "url": "https://example.com/michelin-plant-based",
        "author": "Sophie Laurent",
        "category_slugs": ["lifestyle", "lifestyle-food"],
        "language": "en",
        "region": "europe",
        "raw_tags": ["Michelin", "plant-based", "restaurants", "food"],
    },
    # Crime & Safety
    {
        "title": "International Cybercrime Ring Dismantled in Coordinated Operation",
        "body": "Law enforcement agencies from 12 countries coordinated to dismantle a ransomware network responsible for $300 million in damages. Over 40 suspects were arrested across Europe and Asia.",
        "source": "mock-newsapi",
        "url": "https://example.com/cybercrime-ring-busted",
        "author": "John Carter",
        "category_slugs": ["crime", "tech-cybersecurity"],
        "language": "en",
        "region": "global",
        "raw_tags": ["cybercrime", "ransomware", "Europol"],
    },
]


def generate_mock_articles(
    source_name: str = "mock",
    count: int | None = None,
) -> List[ArticleCreate]:
    """Generate realistic mock articles from seed data.

    If count is None, returns all seed articles for the given source.
    Otherwise returns a random sample of `count` articles.
    """
    now = datetime.now(timezone.utc)
    articles: List[ArticleCreate] = []

    pool = _MOCK_ARTICLES_DATA if not source_name or source_name == "mock" else [
        a for a in _MOCK_ARTICLES_DATA if a.get("source", "").startswith(f"mock-{source_name}")
    ]

    if not pool:
        pool = _MOCK_ARTICLES_DATA

    if count is not None:
        pool = random.sample(pool, min(count, len(pool)))

    for i, entry in enumerate(pool):
        published = now - timedelta(hours=random.randint(1, 72), minutes=random.randint(0, 59))
        articles.append(
            ArticleCreate(
                title=entry["title"],
                body=entry.get("body"),
                summary=entry.get("body", "")[:200] + "..." if entry.get("body") else None,
                url=entry["url"],
                source=source_name or entry.get("source", "mock"),
                author=entry.get("author"),
                language=entry.get("language", "en"),
                region=entry.get("region"),
                raw_tags=entry.get("raw_tags"),
                category_slugs=entry.get("category_slugs"),
                published_at=published,
                content_hash=SourceAdapter.compute_hash(entry["title"], entry["url"]),
            )
        )

    return articles
