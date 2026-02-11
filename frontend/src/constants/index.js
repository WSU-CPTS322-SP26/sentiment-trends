// // Export all constants from a single file
// export { colors } from "./colors";
// export { spacing } from "./spacing";
// export { breakpoints, mediaQueries } from "./breakpoints";
// export { css } from "./css";

// App-specific constants
export const appConfig = {
    name: "Sentiment Trends",
    version: "1.0.0",
    apiUrl: import.meta.env.VITE_API_URL || "http://localhost:5000",
    endpoints: {
        home: "/"
    },
};