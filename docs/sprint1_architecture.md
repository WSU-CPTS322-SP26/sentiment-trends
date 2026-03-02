# Sentiment Trends — Architecture & Current State

> Documents the app as of Sprint 1 (end of Feb 2026). For setup instructions see the root [README](../readme.md).

---

## How the app works right now

The frontend renders a static card grid from mock data. The backend API is live and can fetch posts from Bluesky and Mastodon, but the two sides are not yet connected — no live data flows from the backend to the UI.

```
Browser
  └── React (Vite, port 5001)
        ├── reads mock_data.js  ← current data source
        └── calls GET /         ← health check only

Flask API (port 3001)
  ├── GET /bluesky/search   → atproto → Bluesky
  ├── GET /mastodon/search  → Mastodon.py → Mastodon
  └── (VADER service exists but is not called from any route yet)
```

---

## Frontend

### Pages

| Page             | Route       | Description                                                         |
| ---------------- | ----------- | ------------------------------------------------------------------- |
| `HomePage`       | `/`         | Card grid with category filter and search bar                       |
| `CardDetailPage` | `/card/:id` | Detail view for a single topic (route registered but page is blank) |

### Components

| Component           | What it renders                                                     |
| ------------------- | ------------------------------------------------------------------- |
| `Header`            | App title and `SearchBar`                                           |
| `SearchBar`         | Controlled text input; passes query up to `Header`                  |
| `SearchResultsList` | Dropdown list of matching topics from `mockSearch`                  |
| `SearchResult`      | Single row in the search dropdown                                   |
| `Categories`        | Horizontally scrollable category filter pills                       |
| `Card`              | Topic image, name, category, compound sentiment label, and `Bar`    |
| `Bar`               | Stacked CSS bar: green (positive) / gray (neutral) / red (negative) |

### Data flow (current)

```
mock_data.js
  ├── mockCategories  →  Categories component
  ├── mockSearch      →  SearchResultsList
  └── default export  →  HomePage → Card[]
                                       └── Bar
```

`src/services/api.js` exists as the future home for all backend calls. Right now it only wraps the health check endpoint.

---

## Backend

### Endpoints

| Method | Path                 | Query params                              | Returns                                |
| ------ | -------------------- | ----------------------------------------- | -------------------------------------- |
| GET    | `/`                  | —                                         | `{ "message": "Backend is running" }`  |
| GET    | `/bluesky/timeline`  | `limit`, `cursor`                         | Array of Bluesky posts                 |
| GET    | `/bluesky/search`    | `topic`, `limit`, `cursor`, `sort`, `tag` | Array of Bluesky posts matching topic  |
| GET    | `/mastodon/timeline` | `limit`, `cursor`                         | Array of Mastodon posts                |
| GET    | `/mastodon/search`   | `topic`, `limit`, `cursor`, `sort`, `tag` | Array of Mastodon posts matching topic |

All responses are JSON. Auth failures return `{ "error": "..." }` with status `401`.

### Services

| Module              | Status  | Purpose                                                                                           |
| ------------------- | ------- | ------------------------------------------------------------------------------------------------- |
| `apis/bluesky.py`   | Working | Authenticates with Bluesky via `atproto`; exposes `get_timeline()` and `search_posts()`           |
| `apis/mastodon.py`  | Working | Authenticates with Mastodon; exposes `get_timeline()` and `search_posts()`                        |
| `services/vader.py` | Stub    | Instantiates `SentimentIntensityAnalyzer` and prints a test score — not yet called from any route |

---

## File map

```
sentiment-trends/
├── backend/
│   ├── apis/
│   │   ├── bluesky.py          # Bluesky API client
│   │   └── mastodon.py         # Mastodon API client
│   ├── routes/
│   │   ├── bluesky_routes.py   # /bluesky/* route handlers
│   │   └── mastodon_routes.py  # /mastodon/* route handlers
│   ├── services/
│   │   └── vader.py            # VADER stub (not yet integrated)
│   ├── app.py                  # Flask app factory, CORS, blueprint registration
│   ├── config.py               # Loads credentials from .env
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── mocks/data/
│   │   └── mock_data.js        # Static topic cards, search terms, categories
│   ├── src/
│   │   ├── components/         # Bar, Card, Categories, Header, SearchBar, SearchResult(s)
│   │   ├── pages/              # HomePage, CardDetailPage
│   │   ├── services/
│   │   │   └── api.js          # Fetch wrapper (health check only for now)
│   │   ├── constants/index.js  # Shared constants
│   │   └── App.jsx             # Route definitions
│   ├── index.html
│   ├── vite.config.js
│   └── Dockerfile
├── docs/
│   ├── sprint1_architecture.md         # ← this file
│   └── ui/functionality-plan.md
├── docker-compose.yml          # Spins up both services
├── readme.md                   # Setup + full feature docs
└── sprint1_report.md           # Sprint 1 retrospective
```

---

## What's not wired up yet

- Frontend → Backend: `HomePage` still reads from `mock_data.js`; `api.js` needs search/sentiment endpoints added
- VADER → Routes: `vader.py` needs to be called inside the search route handlers so posts are scored before being returned
- Database: No Supabase integration yet; all data is in-memory and stateless
- Card detail page: `/card/:id` route is registered in `App.jsx` but `CardDetailPage` renders nothing
