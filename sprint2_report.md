# Sprint 2 Report (3/1/2026 - 4/4/2026)

## What's New (User Facing)

- Home page topic cards load real data from the backend: each card shows the latest sentiment snapshot stored in Supabase (positive, neutral, negative bars plus category labels from the database)
- Topic detail route at `/topic/:topic` with on-demand sentiment analysis: compound score, percentage breakdown, stacked bar, and a highlighted top post from Bluesky or Mastodon after each visit
- Search bar still filters a mock suggestion list as you type; pressing Enter or choosing a result navigates to the topic page, which triggers the live analyze call
- Category navigation on the home page is driven by categories present on the loaded cards (no fixed mock list for that path)
- Loading indicator on the topic detail page while analysis is in flight
- Flask endpoints for `GET /supabase/home` (homepage cards) and `GET /sentiment/analyze` (cross-platform fetch plus VADER)
- `scripts/track_topics.py` CLI to pull trending topics via SerpAPI, run the same analysis pipeline, and write topics, daily sentiment rows, and top posts into Supabase
- Expanded automated tests (unit mocks, integration against live APIs when credentials are set, and Supabase-related unit tests)
- Starter GitHub Actions workflow file for scheduled topic tracking (currently commented out; secrets and script path still need to be finalized)

## Work Summary (Developer Facing)

This sprint closed the loop between the UI, the Flask API, VADER, and persistence. The frontend now calls `getHomepageCards()` against `/supabase/home` and maps API fields into the existing card grid, and `TopicDetailPage` calls `getSentimentAnalysis()` on `/sentiment/analyze` for a fresh Bluesky and Mastodon pull scored in `services/sentiment.py`. Supabase is configured in `config.py`; `db/homepage.py` shapes nested `daily_topic_sentiment` rows for the home response. SerpAPI powers `apis/topics.py` for trending discovery, and `track_topics.py` upserts `topics`, inserts `daily_topic_sentiment`, and replaces `top_posts` per run. Tailwind was added for the topic detail layout alongside existing CSS Modules. The main remaining pain points are incomplete automation (#21), deeper DB tests (#28), mock-only search suggestions, and the topic page still using mock data for header category links.

## Unfinished Work

The UI is not finished: layout and styling are still inconsistent in places, and the product does not yet feel like a single polished experience. Only the home page is fully wired to backend-driven card data (`GET /supabase/home`); the header search and category strip on other views still rely on mock data, and the topic detail screen depends on on-demand `GET /sentiment/analyze` rather than the same Supabase snapshot feed as the grid. We still need a real source for topic images; cards use a shared placeholder asset instead of per-topic artwork or thumbnails from an API or stored URLs. The GitHub Actions workflow in [.github/workflows/track_topics.yml](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/.github/workflows/track_topics.yml) is commented out and still pointed at an old module path in places, so routine server-side runs of `track_topics.py` are not production-ready. Issue [#28 DB tests](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/28) remains open for broader database test coverage. Header search does not call the backend for live topic lookup. Topic detail analysis is strictly on-demand per navigation and does not reuse homepage snapshots. The topic detail header categories still come from mock data, and the mix of Tailwind and CSS Modules is not fully unified.

## Completed Issues/User Stories

- [#14 Topic Page](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/14)
- [#16 Assign categories to trending cards](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/16)
- [#18 Category navigation](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/18)
- [#19 Card detail page](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/19)
- [#20 Vader Sentiment](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/20)
- [#22 Supabase config](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/22)
- [#23 Live sentiment analyisis](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/23)
- [#24 Frontend searching using backend analyze endpoint](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/24)
- [#25 Connect analyze route to frontend for searchbar](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/25)
- [#26 Backend tests](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/26)
- [#27 Tests](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/27)
- [#30 Find a reliable source for trending topics](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/30)
- [#31 Create loading transition](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/31)
- [#32 Style topic detail page](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/32)
- [#33 Topic detail page charts](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/33)
- [#34 load supabase in config.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/34)
- [#35 Backend home routes](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/35)
- [#36 Topics](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/36)
- [#37 Topic page](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/37)
- [#38 Supabase home](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/38)
- [#39 Frontend categories](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/39)
- [#40 homepage route](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/40)
- [#41 Frontend home uses backend route](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/41)
- [#42 Loading icon](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/42)

## Incomplete Issues/User Stories

- [#21 GitHub Actions Script](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/21)
- [#28 DB tests](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/28)

## Code Files for Review

**Backend API and services**

- [apis/topics.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/apis/topics.py)
- [apis/bluesky.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/apis/bluesky.py)
- [apis/mastodon.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/apis/mastodon.py)
- [config.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/config.py)
- [db/homepage.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/db/homepage.py)
- [db/**init**.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/db/__init__.py)
- [routes/supabase_routes.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/routes/supabase_routes.py)
- [routes/sentiment_routes.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/routes/sentiment_routes.py)
- [routes/**init**.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/routes/__init__.py)
- [services/sentiment.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/services/sentiment.py)
- [services/bluesky_topics.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/services/bluesky_topics.py)
- [utils/helpers.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/utils/helpers.py)

**Scripts and automation**

- [scripts/track_topics.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/scripts/track_topics.py)
- [.github/workflows/track_topics.yml](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/.github/workflows/track_topics.yml)

**Frontend**

- [App.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/App.jsx)
- [pages/HomePage.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/pages/HomePage.jsx)
- [pages/TopicDetailPage.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/pages/TopicDetailPage.jsx)
- [services/api.js](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/services/api.js)
- [constants/index.js](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/constants/index.js)
- [components/Card.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/components/Card.jsx)
- [components/Loader.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/components/Loader.jsx)
- [components/Bar.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/components/Bar.jsx)
- [styles/pages/TopicDetailPage.module.css](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/styles/pages/TopicDetailPage.module.css)
- [vite.config.js](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/vite.config.js)
- [package.json](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/package.json)

**Tests**

- [tests/unit/test_supabase_routes.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/tests/unit/test_supabase_routes.py)
- [tests/unit/test_homepage_db.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/tests/unit/test_homepage_db.py)
- [tests/conftest.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/tests/conftest.py)
- [tests/integration/conftest.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/tests/integration/conftest.py)

**Project docs and env**

- [README.md](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/README.md)
- [backend/.env.example](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/.env.example)

## Retrospective Summary

Here's what went well:

- Supabase and the analyze route gave us a clear split between stored homepage snapshots and fresh per-topic analysis
- `track_topics.py` made it possible to seed and refresh real card data without manual SQL
- pytest coverage grew with both mocked unit tests and optional integration runs against Bluesky and Mastodon
- Docker Compose still gives a one-command dev environment after adding new Python dependencies

Here's what we'd like to improve:

- Finish and verify GitHub Actions so scheduled runs match `scripts/track_topics.py` and repository secrets
- Close out [#28](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/28) with stronger tests around Supabase access patterns
- Replace mock search with a real topic list or query endpoint when requirements are clear
- Align styling so topic detail and home feel like one design system

Here are changes we plan to implement in the next sprint:

- Turn on the workflow (or replace it) so topic tracking runs on a schedule with correct env and working directory
- Backend-driven search or autocomplete wired from Supabase or a dedicated route
- Optional caching or reuse of stored sentiment on the topic page where it makes sense for UX
- Richer charts or history on the topic page if time allows

**Note:** [#17 Trending Topic Browser Caching](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/17) and [#29 Migrate css modules to Tailwind](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/29) were closed as not planned during this period; we partially addressed styling with Tailwind on the topic page instead of a full migration.

## Demo Video

[https://www.youtube.com/watch?v=QAsLqgFsTmk&feature=youtu.be](https://www.youtube.com/watch?v=QAsLqgFsTmk&feature=youtu.be)
