# Sentiment Trends

## Summary

A social media sentiment analysis dashboard that fetches posts from Bluesky and Mastodon, scores them with VADER, and visualizes positive/negative/neutral sentiment trends across trending topics.

### Additional information

Sentiment Trends lets you track how the internet feels about any up-to-date topic. Pick a subject and the app queries Bluesky and Mastodon, runs every post through the VADER sentiment engine, and renders a card showing the breakdown of positive, neutral, and negative sentiment.

The frontend is a React application (Vite, CSS Modules, and Tailwind on some screens) with routing to a topic detail view. The backend is a Flask REST API with Bluesky/Mastodon clients, a Supabase-backed homepage endpoint, and a separate on-demand sentiment analysis route. A CLI script (`scripts/track_topics.py`) can pull trending topics, analyze them, and upsert rows into Supabase for the cards you see on the home page. The full stack still spins up with a single Docker Compose command.

> **Note:** The project is in active development. See [Known Issues](#known-issues) for current limitations.

---

## Installation

### Prerequisites

Make sure the following are installed before you begin:

| Tool                                                              | Version | Notes                      |
| ----------------------------------------------------------------- | ------- | -------------------------- |
| [Git](https://git-scm.com/)                                       | any     | for cloning the repo       |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | 24+     | includes Docker Compose v2 |

No local Python or Node runtime is required.

### Add-ons

#### Backend (Python 3.12 / Flask)

| Package          | Purpose                                                                 |
| ---------------- | ----------------------------------------------------------------------- |
| `flask`          | REST API web framework                                                  |
| `flask-cors`     | Allows the frontend origin to call the backend API                      |
| `requests`       | HTTP client for external calls                                        |
| `atproto`        | Bluesky AT Protocol client                                              |
| `Mastodon.py`    | Mastodon API client                                                     |
| `python-dotenv`  | Loads credentials from `.env` into environment variables              |
| `vaderSentiment` | Sentiment analysis                                                      |
| `supabase`       | Supabase client for homepage topics and sentiment snapshots             |
| `pytrends`       | Google Trends client (listed in requirements)                           |
| `serpapi`        | SerpAPI client for trending topic discovery                           |
| `pytest`         | Test runner                                                             |

#### Frontend (Node 20 / React 18)

| Package                   | Purpose                                   |
| ------------------------- | ----------------------------------------- |
| `react` / `react-dom`     | UI component framework                    |
| `react-router-dom`        | Client-side routing                       |
| `react-icons`             | Icon set (search icon in the header bar)  |
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

# SerpAPI: used by trending-topic discovery 
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

Both containers mount their source directories as live volumes, so any edits you make locally are reflected immediately (Flask `--reload`, Vite HMR with filesystem polling).

#### 5. Stopping the stack

```bash
docker compose down
```

---

## Functionality

### Browsing topic cards

The home page loads topic cards from the backend (`GET /supabase/home`). Each card shows:

- A placeholder image for the topic
- The topic name and category label(s)
- A stacked sentiment bar for positive (green), neutral (gray), and negative (red) using the **latest snapshot** stored in Supabase

The grid only shows what is already in Supabase; use the **track topics script** (below) to ingest trending topics and sentiment snapshots.

### Track topics script

[scripts/track_topics.py](scripts/track_topics.py) is a command-line job you run locally (it is not started by Docker Compose). It keeps the homepage database in sync with “what’s trending” plus fresh sentiment aggregates.

1. **Trending list**: Calls SerpAPI (`SERPAPI_KEY` in `backend/.env`) for the current trending-now style topic list, capped by `--max-topics`.
2. **`topics` table**: Upserts each trend by name into Supabase, including optional search volume, increase percentage, and category labels from the API when present.
3. **Sentiment pass**: For each topic, runs the same Bluesky + Mastodon fetch and VADER scoring used by `GET /sentiment/analyze` (`analyze_topic` in the backend), with per-platform limits you can tune.
4. **`daily_topic_sentiment`**: Inserts one snapshot row per topic for that run (all rows share the same batch timestamp).
5. **`top_posts`**: Deletes existing rows for that topic and inserts the top posts returned by the analyzer for that run.

CLI flags (each has a default inside the script): `--max-topics`, `--bluesky-limit`, `--mastodon-limit`, `--top-n`. If one topic fails, the error is logged and the script continues with the rest.

Run from the **repository root** with Python 3.12+ and backend dependencies installed, and a filled-in `backend/.env` (Supabase, SerpAPI, Bluesky, Mastodon):

```bash
pip install -r backend/requirements.txt
python scripts/track_topics.py --max-topics 150 --bluesky-limit 1000 --mastodon-limit 100 --top-n 5
```

The script loads `backend/.env` automatically and adjusts `sys.path` so backend imports resolve.

### Filtering by category

A horizontally scrollable category nav sits below the header. Click any category to filter the visible cards to that category. Click **All** to reset.

### Searching for a topic

The header search bar filters a **fixed mock suggestion list** as you type ([SearchBar.jsx](frontend/src/components/SearchBar.jsx)); it does **not** query the backend for live topic search results. Pressing **Enter** with a non-empty query navigates to `/topic/...`, where sentiment is computed **on demand** (see below). Choosing a dropdown suggestion does the same.

### Topic detail (on-demand analysis)

Clicking a card opens `/topic/:topic`. That page calls `GET /sentiment/analyze`, which fetches fresh posts from Bluesky and Mastodon for that topic, scores them with VADER, and returns unified percentages, compound score, and an optional top post. **Nothing on this path reuses the Supabase snapshot**; each visit triggers a new analysis run (subject to API limits and latency).

### Backend API

The Flask backend exposes the following endpoints:

| Method | Endpoint             | Query params                                                                 | Description                                                          |
| ------ | -------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| GET    | `/`                  |                                                                               | Health check                                                         |
| GET    | `/supabase/home`     |                                                                               | Homepage cards: topics plus latest `daily_topic_sentiment` from DB   |
| GET    | `/sentiment/analyze` | `topic` or `q`, `limit`, `top_n`, optional `bluesky_limit`, `mastodon_limit` | On-demand cross-platform fetch + VADER aggregation                   |
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

1. **Search is not backed by live data**: The typeahead only filters [mock_data.js](frontend/mocks/data/mock_data.js). There is no API-driven topic search; “on demand” here means you either pick a mock suggestion or type a string and press Enter, which only then loads the topic page and runs analysis.

2. **Topic detail is strictly on-demand**: Each visit to `/topic/:topic` calls `/sentiment/analyze` and re-fetches posts from Bluesky/Mastodon. Results are not cached in the browser for repeat visits, and this path does not read the same Supabase snapshot that powers the home cards.

3. **UI is incomplete and inconsistent**: The home page is primarily CSS Modules; the topic detail view mixes modules with Tailwind-style utility classes. Category navigation on the detail page is still derived from mock data ([TopicDetailPage.jsx](frontend/src/pages/TopicDetailPage.jsx)), not from the same live card list as the home page. Card images are placeholders.

4. **Homepage requires Supabase data**: If `topics` / nested sentiment rows are empty or credentials are wrong, the grid will be empty or error. There is no in-app admin flow to add topics; use scripts or direct DB work.

5. **Major social platforms are inaccessible**: Reddit's API and Twitter/X's API are effectively closed to free or hobbyist use (high cost, restrictive terms, or revoked access). The app currently targets Bluesky and Mastodon as open alternatives. A workaround strategy for broader platform coverage is still to be determined.

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
