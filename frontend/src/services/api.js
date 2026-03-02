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
};