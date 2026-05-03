# Sprint 3 Report (4/5/2026 - 5/2/2026)

## What's New (User Facing)

- Stored Supabase snapshots on the topic page via `GET /supabase/topic` (latest saved sentiment bars, categories, search volume, trend percentage, and ranked top posts alongside the existing live analyze path from Sprint 2)
- AI-generated summary block on the topic page backed by an Ollama-friendly `/ollama/summary` route that reuses the same analyzed posts as the rest of the pipeline (falls back gracefully when the summarizer is unavailable)
- Per-topic card artwork when SerpAPI returns Google Images results during tracking; homepage cards display those URLs plus hover polish and clearer volume or trend callouts
- Skeleton placeholders for the home grid and topic detail first paint, in addition to the existing topic page loading behavior from Sprint 2
- About page with favicon and refreshed navigation plus logo-driven header branding across light layouts
- Dark and light themes with session persistence, OS preference as default, matching logos, and styled search and topic detail areas for both modes
- Improved layout on small screens so headers and the topic detail page remain usable on mobile viewports
- GitHub Actions workflow that deploys the backend on pushes to `main` using Tailscale and SSH to the hosted server

## Work Summary (Developer Facing)

On top of the Flask, VADER, SerpAPI trending, and Supabase wiring already described for Sprint 2, this sprint added `db/topic_detail.py` and `GET /supabase/topic`, optional `/ollama/summary` via `services/summary.py` and `ollama_routes.py`, Google Images fetching in `apis/images.py`, image URL persistence through `scripts/track_topics.py` (same script path Sprint 2 introduced), compose overrides for Ollama, and frontend glue (`getTopicDetailFromDb`, `getOllamaSummary`, skeleton components, theme tokens, About route). Deployment automation added [.github/workflows/deploy.yml](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/.github/workflows/deploy.yml). The scheduled [.github/workflows/track_topics.yml](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/.github/workflows/track_topics.yml) workflow remained commented with the outdated module path noted in Sprint 2.

## Unfinished Work

Search autocomplete still draws from a limited client-side list rather than a comprehensive backend index ([#47 Better search autocomplete](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/47)). Issue [#28 DB tests](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/28) stays open for deeper coverage of Supabase read and write paths in CI. Topic-level enhancements discussed mid-sprint remain open: [#61 Display mastodon posts on topic page](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/61), [#62 Omit "No Data" topics from displaying](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/62), and [#63 Graphs](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/63) for historical or trends visualization. The scheduled `track_topics` GitHub Action is still the same open item as in Sprint 2: it must be enabled, retargeted to `scripts/track_topics.py`, and given secrets and a cron so unattended runs match what people do locally. Ollama summarization depends on infrastructure and env wiring in each environment.

## Completed Issues/User Stories

- [#21 GitHub Actions Script](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/21)
- [#43 CI/CD pipeline for automated backend deployment](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/43)
- [#45 Backend topic detail](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/45)
- [#48 AI powered analysis](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/48)
- [#49 Skeleton Loading](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/49)
- [#50 Topic detail](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/50)
- [#51 db pruning](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/51)
- [#52 Llm summary](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/52)
- [#53 Limit cards displayed on homescreen](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/53)
- [#54 skeleton](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/54)
- [#55 fix](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/55)
- [#56 Topic Images](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/56)
- [#57 Images](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/57)
- [#58 Frontend Topic Images](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/58)
- [#59 Images](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/59)
- [#60 Troy frontend](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/60)
- [#64 Dark mode](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/64)
- [#65 mobile viewport](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/65)

**Note:** [#44 quick fix for topic ordering](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/44) and [#46 Frontend changes](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/46) also closed on 4/5/2026; they are treated as Sprint 2 closeout work so this list does not double-count them.

## Incomplete Issues/User Stories

- [#28 DB tests](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/28)
- [#47 Better search autocomplete](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/47)
- [#61 Display mastodon posts on topic page](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/61)
- [#62 Omit "No Data" topics from displaying](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/62)
- [#63 Graphs](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/63)

## Code Files for Review

Paths listed in the [Sprint 2 report](sprint2_report.md) cover the original Flask APIs, `db/homepage.py`, `routes/supabase_routes.py`, `scripts/track_topics.py`, core pages, shared components such as `Card.jsx`, and baseline tests. For Sprint 3, prioritize these **additional or Sprint-3-focused** paths:

**Backend API and services**

- [apis/images.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/apis/images.py)
- [apis/**init**.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/apis/__init__.py)
- [db/topic_detail.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/db/topic_detail.py)
- [routes/ollama_routes.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/routes/ollama_routes.py)
- [services/summary.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/services/summary.py)

**Automation**

- [.github/workflows/deploy.yml](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/.github/workflows/deploy.yml)

**Frontend**

- [pages/AboutPage.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/pages/AboutPage.jsx)
- [components/Header.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/components/Header.jsx)
- [components/CardSkeleton.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/components/CardSkeleton.jsx)
- [components/CardGridSkeleton.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/components/CardGridSkeleton.jsx)
- [components/TopicDetailSkeleton.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/components/TopicDetailSkeleton.jsx)
- [components/TopicDetailPageSkeleton.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/components/TopicDetailPageSkeleton.jsx)
- [utils/HomepageCardsContext.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/utils/HomepageCardsContext.jsx)
- [utils/sentimentTone.js](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/utils/sentimentTone.js)
- [utils/titleCase.js](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/utils/titleCase.js)
- [styles/components/Header.module.css](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/styles/components/Header.module.css)
- [styles/components/Card.module.css](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/styles/components/Card.module.css)
- [styles/components/SearchBar.module.css](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/styles/components/SearchBar.module.css)
- [styles/components/SearchResult.module.css](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/styles/components/SearchResult.module.css)
- [styles/components/SearchResultsList.module.css](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/styles/components/SearchResultsList.module.css)
- [styles/pages/HomePage.module.css](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/styles/pages/HomePage.module.css)
- [styles/pages/AboutPage.module.css](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/styles/pages/AboutPage.module.css)
- [index.css](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/index.css)

**Tests**

- Updates extend the Supabase route and homepage DB tests already linked from Sprint 2; review diffs on [tests/unit/test_supabase_routes.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/tests/unit/test_supabase_routes.py) and [tests/unit/test_homepage_db.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/tests/unit/test_homepage_db.py) with topic detail and image fields in mind.

**Project**

- [docker-compose.yml](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/docker-compose.yml)
- [.gitignore](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/.gitignore)

## Retrospective Summary

Here's what went well:

- `GET /supabase/topic` plus the existing analyze flow gave stable snapshots with optional live analysis and LLM summary
- Image ingestion during tracking replaced placeholder-only cards and made the grid easier to scan
- Skeletons and theme switching materially improved perceived polish without rewriting the whole stack
- Deploy automation closed the gap between merged code and what runs on the hosted backend

Here's what we'd like to improve:

- Finish broader DB testing tracked under [#28](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/28) and exercise Supabase paths in CI the same way developers run them locally
- Replace mock-heavy search with backend-fed suggestions once requirements settle ([#47](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/47))
- Uncomment or replace the scheduled tracking workflow so ingestion stays aligned with `scripts/track_topics.py`

Here are changes we plan to implement in the next sprint:

- Time-series or comparative graphs ([#63](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/63)) and clearer handling of empty or low-quality topics ([#62](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/62))
- Richer topic page coverage across platforms where gaps remain ([#61](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/61))
- Continue hardening deployment and scheduled jobs alongside automated tests

## Demo Video

here
