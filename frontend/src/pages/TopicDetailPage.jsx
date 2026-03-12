import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../services/api";

const TopicDetailPage = () => {
    const { topic } = useParams();
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        api.getSentimentAnalysis(topic)
            .then(setData)
            .catch(setError)
            .finally(() => setLoading(false));
    }, [topic]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    return (
        <div>
            <h1>Sentiment Analysis: {topic.toUpperCase()}</h1>
            {/* TODO: add compound sentiment, this should be an easy fix in the backend to get this added. */}
            <p>Positive: {data?.unified.positive_pct}%</p>
            <p>Neutral: {data.unified.neutral_pct}%</p>
            <p>Negative: {data.unified.negative_pct}%</p>
            Back to <Link to="/">home</Link>
        </div>
    );
};

export default TopicDetailPage;