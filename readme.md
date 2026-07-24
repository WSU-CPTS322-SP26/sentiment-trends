# Sentiment Trends

## Summary

A social media sentiment analysis dashboard that fetches posts from Bluesky and Mastodon, scores them with VADER, stores snapshots in Supabase, and visualizes positive/negative/neutral sentiment trends across trending topics. Optional Ollama-backed summaries describe what people are saying about each topic.

### Additional information

Sentiment Trends lets you track how the internet feels about any up-to-date topic. The home page shows cards from Supabase (latest sentiment snapshot, optional topic images, search volume, and trend percentage). Pick a subject from a card or the search bar and the app opens a topic detail view: if that topic is already tracked it loads the stored snapshot and top posts; otherwise it runs a live Bluesky/Mastodon fetch through VADER. You can generate or view an AI summary when Ollama is available.

The frontend is a React application (Vite, CSS Modules, and Tailwind on some screens) with light/dark themes, an About page, skeleton loading states, and routing to topic detail. The backend is a Flask REST API with Bluesky/Mastodon clients, Supabase-backed homepage and topic endpoints, on-demand sentiment analysis, and an optional Ollama summary route. A CLI script (`scripts/track_topics.py`) pulls trending topics via SerpAPI, analyzes them, optionally fetches images, writes Ollama summaries when configured, and upserts rows into Supabase. The full stack still spins up with a single Docker Compose command.

> **Note:** The project is in active development. See [Known Issues](#known-issues) for current limitations.

---

## Installation

### Prerequisites

Make sure the following are installed before you begin:

| Tool                                                              | Version | Notes                      |
| ----------------------------------------------------------------- | ------- | -------------------------- |
| [Git](https://git-scm.com/)                                       | any     | for cloning the repo       |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | 24+     | includes Docker Compose v2 |

No local Python or Node runtime is required for the Docker stack. Optional: a local [Ollama](https://ollama.com/) instance if you want AI topic summaries.

### Add-ons

#### Backend (Python 3.12 / Flask)

| Package          | Purpose                                                                 |
| ---------------- | ----------------------------------------------------------------------- |
| `flask`          | REST API web framework                                                  |
| `flask-cors`     | Allows the frontend origin to call the backend API                      |
| `requests`       | HTTP client for external calls (including Ollama)                       |
| `atproto`        | Bluesky AT Protocol client                                              |
| `Mastodon.py`    | Mastodon API client                                                     |
| `python-dotenv`  | Loads credentials from `.env` into environment variables              |
| `vaderSentiment` | Sentiment analysis                                                      |
| `supabase`       | Supabase client for homepage topics and sentiment snapshots             |
| `pytrends`       | Google Trends client (listed in requirements)                           |
| `serpapi`        | SerpAPI client for trending topic discovery and optional topic images |
| `pytest`         | Test runner                                                             |

#### Frontend (Node 20 / React 18)

| Package                   | Purpose                                   |
| ------------------------- | ----------------------------------------- |
| `react` / `react-dom`     | UI component framework                    |
| `react-router-dom`        | Client-side routing                       |
| `react-icons`             | Icon set (search, theme toggle, etc.)     |
| `tailwindcss`             | Utility-first styling (topic detail, etc.) |
| `@tailwindcss/vite`       | Tailwind integration for Vite             |
| `vite`                    | Development server and production bundler |
| `@vitejs/plugin-react`    | Vite plugin for React fast-refresh        |

### Installation Steps

#### 1. Clone the repository

```bash
git clone https://github.com/WSU-CPTS322-SP26/sentiment-trends.git
cd sentiment-trends
```

#### 2. Configure environment variables

Copy the example env file and fill in your credentials:

```bash
cp backend/.env.example backend/.env
```

Open `backend/.env` and replace the placeholder values:

```
# Supabase: project URL and service role key
SUPABASE_URL=https://url.supabase.co
SUPABASE_SERVICE_KEY=your_key_here

# SerpAPI: used by trending-topic discovery (and optional topic images)
SERPAPI_KEY=your_serpapi_key_here

# Bluesky: create an App Password at https://bsky.app/settings/app-passwords
BLUESKY_HANDLE=yourhandle.bsky.social
BLUESKY_APP_PASSWORD=your-app-password

# Mastodon: register an application at https://<your-instance>/settings/applications
MASTODON_INSTANCE_URL=https://mastodon.social
MASTODON_CLIENT_KEY=your_client_key
MASTODON_CLIENT_SECRET=your_client_secret
MASTODON_ACCESS_TOKEN=your_access_token
```

Docker Compose also wires optional Ollama settings (defaults shown). Point `OLLAMA_BASE_URL` at a reachable Ollama host if you want summaries:

```
OLLAMA_BASE_URL=http://172.17.0.1:11434
OLLAMA_MODEL=qwen2.5:7b
OLLAMA_TIMEOUT=30
```

> The frontend reads `VITE_API_URL` (defaults to `http://localhost:3001`). No additional frontend env file is needed for local development.

#### 3. Build and start the stack

```bash
docker compose up --build
```

Docker will pull base images, install all Python and Node dependencies, and start both services. On first run this takes ~2 minutes; subsequent starts are faster because layers are cached.

#### 4. Open the app

| Service              | URL                                            |
| -------------------- | ---------------------------------------------- |
| Frontend             | [http://localhost:5001](http://localhost:5001) |
| Backend health check | [http://localhost:3001](http://localhost:3001) |

The backend container mounts `./backend` as a live volume (Flask reloads on code changes). Rebuild the frontend image (or run Vite locally) after frontend edits.

#### 5. Stopping the stack

```bash
docker compose down
```

---

## Functionality

### Browsing topic cards

The home page loads topic cards from the backend (`GET /supabase/home`). Each card shows:

- A topic image when one was stored during tracking, otherwise a placeholder
- The topic name, category label(s), optional search volume, and trend percentage
- A stacked sentiment bar for positive (green), neutral (gray), and negative (red) using the **latest snapshot** stored in Supabase
- An overall tone label derived from the compound score

The grid is paginated and only shows what is already in Supabase; use the **track topics script** (below) to ingest trending topics and sentiment snapshots. Skeleton placeholders appear while cards load. Light and dark themes follow OS preference by default and can be toggled in the header.

### Track topics script

[scripts/track_topics.py](scripts/track_topics.py) is a command-line job you run locally (it is not started by Docker Compose). It keeps the homepage database in sync with "what's trending" plus fresh sentiment aggregates.

1. **Trending list**: Calls SerpAPI (`SERPAPI_KEY` in `backend/.env`) for the current trending-now style topic list, capped by `--max-topics`.
2. **`topics` table**: Upserts each trend by name into Supabase, including optional search volume, increase percentage, and category labels from the API when present. With `--with-images`, also stores SerpAPI image URLs on the topic.
3. **Sentiment pass**: For each topic, runs the same Bluesky + Mastodon fetch and VADER scoring used by `GET /sentiment/analyze` (`analyze_topic` in the backend), with per-platform limits you can tune.
4. **`daily_topic_sentiment`**: Inserts one snapshot row per topic for that run (all rows share the same batch timestamp), including an Ollama summary when the summarizer is reachable.
5. **`top_posts`**: Deletes existing rows for that topic and inserts the top posts returned by the analyzer for that run.
6. **Optional prune**: With `--prune`, removes stale snapshot rows and topics that were not part of the successful run.

CLI flags (each has a default inside the script): `--max-topics`, `--bluesky-limit`, `--mastodon-limit`, `--top-n`, `--with-images`, `--image-n`, `--prune`. If one topic fails, the error is logged and the script continues with the rest.

Run from the **repository root** with Python 3.12+ and backend dependencies installed, and a filled-in `backend/.env` (Supabase, SerpAPI, Bluesky, Mastodon):

```bash
pip install -r backend/requirements.txt
python scripts/track_topics.py --max-topics 25 --bluesky-limit 300 --mastodon-limit 100 --top-n 5 --with-images --image-n 3
```

The script loads `backend/.env` automatically and adjusts `sys.path` so backend imports resolve.

### Filtering by category

A horizontally scrollable category nav sits below the header. Categories are derived from the live homepage card list. Click any category to filter the visible cards to that category. Click **All** to reset.

### Searching for a topic

The header search bar filters the **loaded homepage cards** as you type ([SearchBar.jsx](frontend/src/components/SearchBar.jsx)); it does **not** query a dedicated backend search index. Pressing **Enter** with a non-empty query navigates to `/topic/...`. Choosing a dropdown suggestion does the same. Topics already in Supabase open from the stored snapshot; unknown queries fall through to live analysis on the topic page.

### Topic detail (stored snapshot or on-demand analysis)

Clicking a card opens `/topic/:topic`. That page first calls `GET /supabase/topic`. On a hit it shows the stored sentiment percentages, compound score, snapshot time, top posts, and any saved summary. On a miss it calls `GET /sentiment/analyze`, which fetches fresh posts from Bluesky and Mastodon, scores them with VADER, and returns unified percentages, compound score, and top posts. If no summary is stored, **Generate Summary** calls `GET /ollama/summary` (returns 503 when Ollama is unavailable).

### Backend API

The Flask backend exposes the following endpoints:

| Method | Endpoint             | Query params                                                                 | Description                                                          |
| ------ | -------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| GET    | `/`                  |                                                                               | Health check                                                         |
| GET    | `/supabase/home`     |                                                                               | Homepage cards: topics plus latest `daily_topic_sentiment` from DB   |
| GET    | `/supabase/topic`    | `id` or `topic` / `q`                                                         | One topic row with latest snapshot and stored `top_posts`            |
| GET    | `/sentiment/analyze` | `topic` or `q`, `limit`, `top_n`, optional `bluesky_limit`, `mastodon_limit` | On-demand cross-platform fetch + VADER aggregation                   |
| GET    | `/ollama/summary`    | `topic` or `q`, `limit`, `top_n`                                              | On-demand analyze + Ollama summary (503 if summarizer unavailable)   |
| GET    | `/bluesky/timeline`  | `limit`, `cursor`                                                             | Authenticated Bluesky home timeline                                  |
| GET    | `/bluesky/search`    | `topic`, `limit`, `cursor`, `sort`, `tag`                                     | Search Bluesky posts by topic                                        |
| GET    | `/mastodon/timeline` | `limit`, `cursor`                                                             | Authenticated Mastodon home timeline                                 |
| GET    | `/mastodon/search`   | `topic`, `limit`, `cursor`, `sort`, `tag`                                     | Search Mastodon posts by topic                                       |

All endpoints return JSON. Authentication errors return `{"error": "..."}` with a `401` status.

---

## Testing

Backend tests are split into **unit** (mock only, no external calls) and **integration** (real remote APIs when credentials are set). Run them from the `backend` directory.

**Unit tests (CI default; no secrets required):**

```bash
cd backend
python -m pytest tests -m unit -v
```

**Integration tests (hits Bluesky/Mastodon when credentials are in env):**

```bash
cd backend
python -m pytest tests -m integration -v
```

**Run all tests:**

```bash
cd backend
python -m pytest tests -v
```

---

## Known Issues

1. **Search is not a full backend index**: Typeahead only filters the homepage cards already loaded in the client. There is no dedicated API-driven topic search across the full database or the open web; typing an arbitrary string and pressing Enter still works by opening the topic page (DB hit or live analysis).

2. **Live topic detail is uncached**: When a topic is missing from Supabase, `/topic/:topic` calls `/sentiment/analyze` and re-fetches posts from Bluesky/Mastodon. Those live results are not written back to the browser cache or Supabase for repeat visits. Tracked topics use the stored snapshot instead.

3. **UI still mixed styling**: The home page is primarily CSS Modules; the topic detail view mixes modules with Tailwind utility classes. Card images fall back to a placeholder when tracking was run without `--with-images` or when image URLs fail to load.

4. **Homepage requires Supabase data**: If `topics` / nested sentiment rows are empty or credentials are wrong, the grid will be empty or error. There is no in-app admin flow to add topics; use `scripts/track_topics.py` or direct DB work. The scheduled GitHub Action for that script is still commented out.

5. **Major social platforms are inaccessible**: Reddit's API and Twitter/X's API are effectively closed to free or hobbyist use (high cost, restrictive terms, or revoked access). The app currently targets Bluesky and Mastodon as open alternatives. A workaround strategy for broader platform coverage is still to be determined. Ollama summaries also depend on a reachable model host and are optional.

---

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

---

## Additional Documentation

[![branch: docs](https://img.shields.io/badge/branch-docs-blue)](https://github.com/WSU-CPTS322-SP26/sentiment-trends/tree/docs)

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for the full text.
