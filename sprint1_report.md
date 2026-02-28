# Sprint 1 Report (1/12/2026 - 2/28/2026)

## What's New (User Facing)

- Topic card grid on the home page displaying sentiment breakdown bars (positive, neutral, negative) per topic
- Category filter nav allowing users to filter visible topic cards by category
- Search bar in the header that filters a list of available topics in real time
- Flask REST API with health check, Bluesky search/timeline, and Mastodon search/timeline endpoints
- Full Docker Compose setup allowing the entire stack to launch with a single command

## Work Summary (Developer Facing)

This sprint focused on laying the structural foundation for the project. In the frontend there is a React (Vite) application with a searchable, category-filtered card grid that renders topic sentiment using stacked bar components. All UI is currently backed by mock data so the design and layout could be built on independently of the backend. In the backend, we set up a Flask REST API with working routes for Bluesky and Mastodon, handling authentication and post fetching for both platforms. We also integrated VADER sentiment as a standalone service and containerized the full stack with Docker Compose. The biggest barrier this sprint was discovering that Reddit and Twitter/X APIs are effectively inaccessible without paying significant fees, so we pivoted to Bluesky and Mastodon as our primary data sources for now.

## Unfinished Work

The frontend is not yet wired to the live backend; all card data comes from a mock data file. The VADER sentiment service exists but is not called by any route or integrated into the API response pipeline. There is no database set up yet, so no data is persisted between requests. These items were not completed because we prioritized getting the UI design and API structure established first.

## Completed Issues/User Stories

- [https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/4](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/1)
- [https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/5](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/2)
- [https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/8](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/3)
- [https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/13](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/3)

## Incomplete Issues/User Stories

- [https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/14](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/4) 
- [https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/16](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/5) 
- [https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/17](https://github.com/WSU-CPTS322-SP26/sentiment-trends/issues/6) 

## Code Files for Review

- [bluesky.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/apis/bluesky.py)
- [mastodon.py](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/backend/apis/mastodon.py)
- [HomePage.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/pages/HomePage.jsx)
- [Card.jsx](https://github.com/WSU-CPTS322-SP26/sentiment-trends/blob/main/frontend/src/components/Card.jsx)

## Retrospective Summary

Here's what went well:

- The Docker Compose setup makes onboarding and running the project straightforward for all team members
- Frontend component architecture is clean and easy to extend
- The backend is able to easily get data so sentiment analysis will be completed in no time

Here's what we'd like to improve:

- Quicker resolutions to road blocks (like with the Twitter and Reddit API issues)
- Focus on immediate app needs and not future additions
- Better spread of workload between frontend and backend between all members

Here are changes we plan to implement in the next sprint:

- Wire the frontend to live backend endpoints and remove mock data
- Integrate VADER sentiment scoring into the API so cards display real sentiment data
- Set up Supabase database to persist fetched posts and computed scores
- Set up github actions to routinely fetch and analyze data

