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

// Specific API functions
export const api = {
    // Get home message
    getHomeMessage: () => apiRequest(appConfig.endpoints.home),
    // Get Sentiment Analysis data
    getSentimentAnalysis: (topic, limit = 25, top_n = 5) => 
        apiRequest(`${appConfig.endpoints.sentimentAnalysis}?topic=${encodeURIComponent(topic)}&limit=${limit}&top_n=${top_n}`)
};