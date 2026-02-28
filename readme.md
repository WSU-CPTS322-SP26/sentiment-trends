# Sentiment Trends

## Summary

A social media sentiment analysis dashboard that fetches posts from Bluesky and Mastodon, scores them with VADER, and visualizes positive/negative/neutral sentiment trends across trending topics.

### Additional information

Sentiment Trends lets you track how the internet feels about any up-to-date topic. Pick a subject and the app queries Bluesky and Mastodon, runs every post through the VADER sentiment engine, and renders a card showing the breakdown of positive, neutral, and negative sentiment.

The frontend is a fast, responsive React application (Vite + CSS Modules) organized around a searchable, category-filtered card grid. The backend is a lightweight Flask REST API that authenticates with both social platforms, fetches posts on demand, and will pipe results through VADER before returning scored data to the UI. The full stack spins up with a single Docker Compose command.

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


| Package          | Purpose                                                  |
| ---------------- | -------------------------------------------------------- |
| `flask`          | REST API web framework                                   |
| `flask-cors`     | Allows the frontend origin to call the backend API       |
| `atproto`        | Bluesky AT Protocol client                               |
| `Mastodon.py`    | Mastodon API client                                      |
| `python-dotenv`  | Loads credentials from `.env` into environment variables |
| `vaderSentiment` | Sentiment analysis                                       |


#### Frontend (Node 20 / React 18)


| Package                | Purpose                                   |
| ---------------------- | ----------------------------------------- |
| `react` / `react-dom`  | UI component framework                    |
| `react-router-dom`     | Client-side routing                       |
| `react-icons`          | Icon set (search icon in the header bar)  |
| `vite`                 | Development server and production bundler |
| `@vitejs/plugin-react` | Vite plugin for React fast-refresh        |


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
# Bluesky — create an App Password at https://bsky.app/settings/app-passwords
BLUESKY_HANDLE=yourhandle.bsky.social
BLUESKY_APP_PASSWORD=your-app-password

# Mastodon — register an application at https://<your-instance>/settings/applications
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

The home page displays a grid of topic cards. Each card shows:

- A representative image for the topic
- The topic name and category label
- A stacked sentiment bar broken into positive (green), neutral (gray), and negative (red) segments

### Filtering by category

A horizontally scrollable category nav sits below the header. Click any category to filter the visible cards to that category. Click **All** to reset.

### Searching for a topic

Type in the search bar in the header to filter a list of available topics. Click a result to select it (currently navigates to a detail view. See [Known Issues](#known-issues)).

### Backend API

The Flask backend exposes the following endpoints:


| Method | Endpoint             | Query params                              | Description                          |
| ------ | -------------------- | ----------------------------------------- | ------------------------------------ |
| GET    | `/`                  |                                           | Health check                         |
| GET    | `/bluesky/timeline`  | `limit`, `cursor`                         | Authenticated Bluesky home timeline  |
| GET    | `/bluesky/search`    | `topic`, `limit`, `cursor`, `sort`, `tag` | Search Bluesky posts by topic        |
| GET    | `/mastodon/timeline` | `limit`, `cursor`                         | Authenticated Mastodon home timeline |
| GET    | `/mastodon/search`   | `topic`, `limit`, `cursor`, `sort`, `tag` | Search Mastodon posts by topic       |


All endpoints return JSON. Authentication errors return `{"error": "..."}` with a `401` status.

---

## Known Issues

1. **Frontend uses mock data**: `[HomePage.jsx](frontend/src/pages/HomePage.jsx)` renders cards from `[mocks/data/mock_data.js](frontend/mocks/data/mock_data.js)` and no live calls to the backend are made from the UI. `[src/services/api.js](frontend/src/services/api.js)` exists but is only wired to the health check endpoint, not to search or sentiment flows.
2. **Backend doesn't analyze sentiment yet**: `[backend/services/vader.py](backend/services/vader.py)` is a standalone test script that prints a score to the console. It has not been called from any route or applied to fetched posts, so no sentiment data is generated at runtime.
3. **No database integration**: There is no Supabase database connected yet. Fetched posts and computed sentiment scores are not persisted anywhere; everything is stateless and in-memory.
4. **Major social platforms are inaccessible**: Reddit's API and Twitter/X's API are effectively closed to free or hobbyist use (high cost, restrictive terms, or revoked access). The app currently targets Bluesky and Mastodon as open alternatives. A workaround strategy for broader platform coverage is still to be determined.
5. **No card detail page**: `[Card.jsx](frontend/src/components/Card.jsx)` links to `/card/:id` but that route is not registered in `[App.jsx](frontend/src/App.jsx)`, so clicking a card leads to a blank page.
6. **Search result click is a no-op**: Clicking a search result currently triggers a browser `alert()` with the term name instead of navigating or fetching live data.

---

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

---

## Additional Documentation

---

## License

This project is licensed under the MIT License. See `[LICENSE](LICENSE)` for the full text.