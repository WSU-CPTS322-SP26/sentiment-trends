// App-specific constants
export const appConfig = {
    name: "Sentiment Trends",
    contactEmail: "sentimentrends@gmail.com",
    repoUrl: "https://github.com/WSU-CPTS322-SP26/sentiment-trends",
    issueTicketURL: "https://docs.google.com/forms/d/e/1FAIpQLSd0W41DxyoZESngt5zKFUd5VdfQLRtyLCy8lW4_sTMoAfHcwg/viewform?usp=header",
    version: "1.0.0",
    apiUrl: import.meta.env.VITE_API_URL || "http://localhost:3001",
    endpoints: {
        home: "/",
        sentimentAnalysis: "/sentiment/analyze",
        supabaseHome: "/supabase/home",
    },
};
