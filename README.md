# Syndra

**AI-Powered Universal Multilingual News Platform**

Syndra aggregates trustworthy news across **every domain worldwide** from 15+ global sources, detects content bias with AI, summarizes articles multilingually, maps relevant content to UN SDGs, and recommends articles adaptively — all through an accessible, mobile-first interface.

Energy & Sustainability remains a featured vertical with SDG tracking, but Syndra covers **all fields**: politics, business, technology, science, health, sports, entertainment, and more.

---

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────────────┐
│   Frontend  │───▶│   FastAPI    │──▶│  PostgreSQL + Redis    │
│  React + TS │    │   Backend    │    │  (data + cache)        │
│  Vite + TW  │    │              │    └────────────────────────┘
└─────────────┘    │  NLP Pipeline│───▶ Hugging Face Inference API
                   │  Aggregator  │───▶ NewsAPI / Guardian / RSS / ...
                   └──────────────┘
```

**Frontend:** React 18 · TypeScript · Vite · Tailwind CSS · React Router · TanStack Query
**Backend:** FastAPI · Python 3.10+ · SQLAlchemy 2.0 · Alembic · APScheduler
**AI/NLP:** Hugging Face Inference API (bias detection, summarization, SDG mapping, category classification)
**Data:** PostgreSQL 16 · Redis 7
**DevOps:** Docker Compose · GitHub Actions CI

---

## News Categories

Syndra uses a **hierarchical, data-driven category taxonomy** stored in the database (not hardcoded in the UI). Categories are seeded on startup and extensible without code changes.

**Top-level categories include:**
World, Politics & Government, Business & Finance, Technology, Science, Health & Medicine, Environment & Climate, **Energy & Sustainability** (SDG-aligned), Education, Law & Justice, Crime & Safety, Sports, Entertainment, Arts & Culture, Lifestyle, Automotive, Real Estate, Religion & Faith, Opinion & Editorial, Local & Regional, Breaking News

Each top-level category has **sub-categories** (e.g. Technology → AI, Software, Hardware, Cybersecurity, Social Media).

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 22+
- Cloud Database: **Supabase** (PostgreSQL) & **Upstash** (Redis)

### 1. Clone & configure

```bash
git clone <repo-url> && cd syndra
cp .env.example .env
```
Edit `.env` and fill in your Supabase and Upstash connection strings. (All other API keys are optional).

### 2. Setup Database (Create Tables)

Since the database is hosted on the cloud, run this once to create the tables:
```bash
cd backend
python -m venv venv
# Windows: .\venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# Create the tables in your cloud database
python -c "
import asyncio
from app.core.database import engine
from app.models.base import Base
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Tables created successfully!')
asyncio.run(init_models())
"
cd ..
```

### 3. Run Backend & Frontend (Single Terminal)

From the project root directory, install dependencies and run both servers simultaneously using `concurrently`:

```bash
npm install
npm run dev
```

* Backend runs at: [http://localhost:8000/docs](http://localhost:8000/docs)
* Frontend runs at: [http://localhost:5173](http://localhost:5173)

### 5. Deployment

**Backend (Docker / Render / Railway):**
A `Dockerfile` is provided in the `backend/` directory. You can deploy it directly to any container-hosting platform. Remember to set the environment variables (especially `DATABASE_URL` and `REDIS_URL`) in your hosting dashboard.

**Frontend (Vercel / Netlify):**
The frontend is a standard Vite React app. A `vercel.json` is included for easy deployment.
1. Connect your GitHub repo to Vercel.
2. Set the Build Command to `npm run build` and Output Directory to `dist`.
3. Set the Environment Variable `VITE_API_URL` to point to your deployed backend URL.

```bash
# Backend
cd backend && pytest -v

# Frontend
cd frontend && npm run lint && npx tsc --noEmit
```

---

## Project Structure

```
syndra/
├── frontend/                # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Route pages
│   │   ├── hooks/           # Custom React hooks (health, categories, ...)
│   │   ├── lib/             # Utilities, API client, types
│   │   ├── App.tsx          # Root component + routing
│   │   └── main.tsx         # Entry point
│   └── ...
├── backend/                 # FastAPI + Python
│   ├── app/
│   │   ├── api/routes/      # API endpoints (health, categories, news)
│   │   ├── core/            # Config, database, seed data
│   │   ├── models/          # SQLAlchemy models (Article, Category)
│   │   ├── schemas/         # Pydantic schemas
│   │   └── services/        # Business logic + source adapters
│   │       └── adapters/    # Pluggable news source adapters
│   ├── alembic/             # DB migrations
│   ├── tests/               # Pytest tests
│   └── requirements.txt
├── docker-compose.yml       # PostgreSQL + Redis
├── .env.example             # Environment template
├── .github/workflows/       # CI pipeline
└── README.md
```

---

## Key Design Decisions

- **Data-driven taxonomy**: Categories live in the DB, seeded on startup. No hardcoded category lists in the UI — the frontend fetches `/api/categories` and renders dynamically.
- **Multi-category articles**: Articles link to categories via a many-to-many relationship, supporting multi-label classification.
- **SDG mapping is optional**: Only articles relevant to energy/sustainability get SDG tags — it's a derived enrichment, not a universal requirement.
- **SourceAdapter pattern**: Every news source implements the same interface with mock/seed fallback when API keys are missing.
- **Universal AI pipeline**: Bias detection, summarization, and category classification work across all domains and languages, not just energy.

---

## Environment Variables

All API keys are **optional** — the app uses realistic mock/seed data when keys are missing.

See [`.env.example`](.env.example) for the full list.

---

## Development Roadmap

- [x] **Phase 0** — Project scaffold, hello world end-to-end
- [x] **Phase 1** — Data layer & news aggregation (15+ sources, all categories)
- [x] **Phase 2** — Core frontend (news feed, category navigation, filters, search, i18n)
- [x] **Phase 3** — AI bias detection engine (universal, all domains)
- [x] **Phase 4** — Summarization (RAG) + SDG mapping (energy vertical) + category classifier
- [x] **Phase 5** — Personalization, auth, glossary, TTS, full i18n (10+ languages)
- [x] **Phase 6** — Hardening, tests, deploy, observability

---

## License

MIT
