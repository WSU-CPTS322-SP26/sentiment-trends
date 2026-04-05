import { useParams, Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../services/api";
import styles from "../styles/pages/TopicDetailPage.module.css";
import Header from "../components/Header";
import { mockCards, mockCategories } from "../../mocks/data/mock_data";
import { appConfig } from "../constants";
import Bar from "../components/Bar";
import { LuChartBar } from "react-icons/lu";


const TopicDetailPage = () => {
    const { topic } = useParams();
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [results, setResults] = useState([]);
    const predefinedCategories = mockCategories.map(c => c.label);
    const fromCards = [...new Set(mockCards.map(c => c.category))];
    const ordered = [...new Set([...predefinedCategories, ...fromCards])]
        .filter(Boolean)
        .map((label, i) => ({
            id: i,
            label,
            href: label === "All" ? "/" : `/?category=${encodeURIComponent(label)}`
        }));

        
    useEffect(() => {
        setLoading(true);
        setError(null);
        setData(null);

        api.getSentimentAnalysis(topic)
            .then(setData)
            .catch(setError)
            .finally(() => setLoading(false));
    }, [topic]);

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    const compound = data?.unified?.avg_compound;
    const positive = data?.unified?.positive_pct;
    const neutral = data?.unified?.neutral_pct;
    const negative = data?.unified?.negative_pct;

    const topPost = data?.top_posts?.[0];

    function sentimentColor(value) {
    if (value == null || Number.isNaN(value)) return "text-neutral-400";
    if (value < 0) return "text-red-600";
    if (value > 0) return "text-green-600";
    return "text-neutral-900";
    }
    
    return (
        <div className={styles.DetailPage}>
            <Header title={appConfig.name} 
                onSearch={setResults} 
                results={results}
                categories={ordered}
            />
            <div className={`${styles.pageContainer} min-h-screen bg-zinc-50`}>
                <div className={`${styles.content} py-4`}>
                    <div className={`${styles.panel} space-y-4 border-2 border-neutral-200`}>
                        <h1 className="text-3xl font-bold text-neutral-900">
                            Sentiment Analysis: {topic.toUpperCase()}
                        </h1>
                        
                        <div className="rounded-2xl border-2 border-neutral-200 bg-score-tint px-6 py-5 shadow-sm">
                            <p className="text-sm font-bold text-neutral-500">Compound sentiment score</p>
                            <p className={ `mt-1 text-4xl font-semibold tabular-nums ${sentimentColor(compound)}`}>
                                {compound != null ? compound.toFixed(3) : "—"}
                            </p>
                            <p className="mt-2 text-xs font-bold text-neutral-500">Range: -1.0 (most negative) to +1.0 (most positive)</p>
                        </div>

                        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                            <div className="rounded-2xl border-2 border-green-300 bg-green-100 px-4 py-4 shadow-sm">
                                <p className="text-sm font-bold text-green-600">Positive</p>
                                <p className="mt-1 text-3xl font-semibold tabular-nums text-green-600">
                                {positive != null
                                    ? `${Number(positive).toFixed(0)}%`
                                    : "—"}
                                </p>
                            </div>

                            <div className="rounded-2xl border-2 border-neutral-300 bg-neutral-100 px-4 py-4 shadow-sm">
                                <p className="text-sm font-bold text-neutral-900">Neutral</p>
                                <p className="mt-1 text-3xl font-semibold tabular-nums text-neutral-900">
                                {neutral != null
                                    ? `${Number(neutral).toFixed(0)}%`
                                    : "—"}
                                </p>
                            </div>

                            <div className="rounded-2xl border-2 border-red-300 bg-red-100 px-4 py-4 shadow-sm">
                                <p className="text-sm font-bold text-red-600">Negative</p>
                                <p className="mt-1 text-3xl font-semibold tabular-nums text-red-600">
                                {negative != null
                                    ? `${Number(negative).toFixed(0)}%`
                                    : "—"}
                                </p>
                            </div>
                        </div>
                        <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
                            <div className="flex items-center gap-2 mb-3">
                            <LuChartBar className="size-4 text-gray-600" />
                            <span className="text-sm font-medium text-gray-700">Overall Sentiment Distribution</span>
                            </div>
                            <Bar
                                positive={(positive ?? 0) / 100}
                                neutral={(neutral ?? 0) / 100}
                                negative={(negative ?? 0) / 100}
                            />
                        </div>
                        {topPost && (
                        <div className="rounded-xl border border-neutral-200 bg-white p-4 shadow-sm">
                            <p className="text-lg font-bold uppercase tracking-wide text-neutral-900">
                            Top post
                            <span className="ml-2 font-normal normal-case text-neutral-500">
                                (by engagement on {topPost.platform})
                            </span>
                            </p>
                            <p className="mt-2 text-sm font-medium text-neutral-800">@{topPost.author}</p>
                            <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-neutral-700 line-clamp-6">
                            {topPost.text}
                            </p>
                            <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-neutral-500">
                            <span
                                className={`rounded-full px-2 py-0.5 font-medium capitalize ${
                                topPost.label === "positive"
                                    ? "bg-green-100 text-green-800"
                                    : topPost.label === "negative"
                                    ? "bg-red-100 text-red-800"
                                    : "bg-neutral-100 text-neutral-700"
                                }`}
                            >
                                {topPost.label}
                            </span>
                            <span className="tabular-nums">compound {Number(topPost.compound).toFixed(3)}</span>
                            <span className="tabular-nums">
                                {topPost.like_count} likes · {topPost.repost_count} reposts
                            </span>
                            </div>
                            {topPost.url && (
                            <a
                                href={topPost.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="mt-3 inline-block text-sm font-medium text-[var(--color-primary)] underline-offset-2 hover:underline"
                            >
                                View on {topPost.platform} →
                            </a>
                            )}
                        </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TopicDetailPage;