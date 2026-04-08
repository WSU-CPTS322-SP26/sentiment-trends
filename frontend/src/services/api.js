import { appConfig } from "../constants";
// Base URL for API requests
const API_BASE_URL = appConfig.apiUrl;
// Basic API request function
const apiRequest = async (endpoint) => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);
  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }
  return response.json();
};
// same as fetch but returns null on 404 (other errors still throw)
const apiRequestNullIfNotFound = async (endpoint) => {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);
  if (response.status === 404) return null;
  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }
  return response.json();
};


// Specific API functions
export const api = {
  // Get home message
  getHomeMessage: () => apiRequest(appConfig.endpoints.home),
  // Homepage topic cards from Supabase-backed API
  getHomepageCards: () => apiRequest(appConfig.endpoints.supabaseHome),
  // Stored topic row + top_posts from Supabase (by exact topics.name)
  getTopicDetailFromDb: (topic) =>
    apiRequest(
      `${appConfig.endpoints.supabaseTopic}?topic=${encodeURIComponent(topic)}`,
    ),
  // null when topic is not in the database (404); throws on other failures
  getTopicDetailFromDbAllowMissing: (topic) =>
    apiRequestNullIfNotFound(
      `${appConfig.endpoints.supabaseTopic}?topic=${encodeURIComponent(topic)}`,
    ),
  // Same as getTopicDetailFromDb but keyed by topics.id
  getTopicDetailFromDbById: (id) =>
    apiRequest(
      `${appConfig.endpoints.supabaseTopic}?id=${encodeURIComponent(id)}`,
    ),
  // Get Sentiment Analysis data
  getSentimentAnalysis: (topic, limit = 25, top_n = 5) =>
    apiRequest(
      `${appConfig.endpoints.sentimentAnalysis}?topic=${encodeURIComponent(topic)}&limit=${limit}&top_n=${top_n}`,
    ),
  // Generate summary on demand
  getOllamaSummary: (topic, limit = 25, top_n = 5) =>
    apiRequest(
      `${appConfig.endpoints.ollamaSummary}?topic=${encodeURIComponent(topic)}&limit=${limit}&top_n=${top_n}`,
    ),
};