export const appConfig = {
    name: "Sentiment Trends",
    version: "1.0.0",
    apiUrl: import.meta.env.VITE_API_URL || "http://localhost:5000",
    endpoints: {
        home: "/"
    },
};