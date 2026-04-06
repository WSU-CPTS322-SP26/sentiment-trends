import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../services/api";
import styles from "../styles/pages/TopicDetailPage.module.css";
import Header from "../components/Header";
import { appConfig } from "../constants";
import Bar from "../components/Bar";
import { LuChartBar } from "react-icons/lu";
import Loader from "../components/Loader";
import { toTitleCase } from "../utils/helpers";
import { useHomepageCards } from "../utils/HomepageCardsContext";

const TopicDetailPage = () => {
  const { topic: topicParam } = useParams();
  const { navbarCategories } = useHomepageCards();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [results, setResults] = useState([]);

  const topicSlug = topicParam ?? "";
  const displayTitle =
    data?.topic?.title != null && data.topic.title !== ""
      ? data.topic.title
      : topicSlug;

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    setData(null);

    (async () => {
      try {
        const fromDb = await api.getTopicDetailFromDbAllowMissing(topicSlug);
        if (cancelled) return;
        if (fromDb != null) {
          setData({
            source: "db",
            topic: fromDb.topic,
            posts: fromDb.posts ?? [],
          });
          return;
        }
        const live = await api.getSentimentAnalysis(topicSlug, 25, 25);
        if (cancelled) return;
        setData({
          source: "live",
          topic: {
            title: live.topic ?? topicSlug,
            positive_pct: live.unified?.positive_pct,
            neutral_pct: live.unified?.neutral_pct,
            negative_pct: live.unified?.negative_pct,
            avg_compound: live.unified?.avg_compound,
            snapshot_at: null,
          },
          posts: live.top_posts ?? [],
        });
      } catch (e) {
        if (!cancelled) setError(e);
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [topicSlug]);

  if (loading) {
    return (
      <div className={styles.DetailPage}>
        <Header
          title={appConfig.name}
          onSearch={setResults}
          results={results}
          categories={navbarCategories}
        />
        <div className={`${styles.pageContainer} min-h-screen bg-zinc-50`}>
          <div className={`${styles.content} py-4`}>
            <div
              className={`${styles.panel} space-y-4 border-2 border-neutral-200`}
            >
              <h1 className="text-3xl font-bold text-neutral-900">
                Sentiment Analysis: {toTitleCase(topicSlug)}
              </h1>
              <Loader />
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.DetailPage}>
        <Header
          title={appConfig.name}
          onSearch={setResults}
          results={results}
          categories={navbarCategories}
        />
        <div className={`${styles.pageContainer} min-h-screen bg-zinc-50`}>
          <div className={`${styles.content} py-4`}>
            <div
              className={`${styles.panel} space-y-4 border-2 border-neutral-200`}
            >
              <h1 className="text-3xl font-bold text-neutral-900">
                Sentiment Analysis: {toTitleCase(topicSlug)}
              </h1>
              <p className="text-red-600" role="alert">
                {error.message}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // db snapshot or normalized live analyze payload
  const compoundRaw = data?.topic?.avg_compound;
  const compound =
    compoundRaw != null && !Number.isNaN(Number(compoundRaw))
      ? Number(compoundRaw)
      : null;
  const positive = data?.topic?.positive_pct;
  const neutral = data?.topic?.neutral_pct;
  const negative = data?.topic?.negative_pct;
  const posts = data?.posts ?? [];
  const snapshotAt = data?.topic?.snapshot_at;

  function sentimentColor(value) {
    if (value == null || Number.isNaN(value)) return "text-neutral-400";
    if (value < 0) return "text-red-600";
    if (value > 0) return "text-green-600";
    return "text-neutral-900";
  }

  return (
    <div className={styles.DetailPage}>
      <Header
        title={appConfig.name}
        onSearch={setResults}
        results={results}
        categories={navbarCategories}
      />
      <div className={`${styles.pageContainer} min-h-screen bg-zinc-50`}>
        <div className={`${styles.content} py-4`}>
          <div
            className={`${styles.panel} space-y-4 border-2 border-neutral-200`}
          >
            <h1 className="text-3xl font-bold text-neutral-900">
              Sentiment Analysis: {toTitleCase(displayTitle)}
            </h1>
            {data.source === "live" && (
              <p className="text-sm text-amber-800 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2">
                Live analysis: results are fetched on demand and not from the
                database
              </p>
            )}
            {data.source === "db" && snapshotAt && (
              <p className="text-sm text-neutral-500">
                Snapshot: {new Date(snapshotAt).toLocaleString()}
              </p>
            )}

            <div className="rounded-2xl border-2 border-neutral-200 bg-score-tint px-6 py-5 shadow-sm">
              <p className="text-sm font-bold text-neutral-500">
                Compound sentiment score
              </p>
              <p
                className={`mt-1 text-4xl font-semibold tabular-nums ${sentimentColor(compound)}`}
              >
                {compound != null ? compound.toFixed(3) : "—"}
              </p>
              <p className="mt-2 text-xs font-bold text-neutral-500">
                Range: -1.0 (most negative) to +1.0 (most positive)
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
              <div className="rounded-2xl border-2 border-green-300 bg-green-100 px-4 py-4 shadow-sm">
                <p className="text-sm font-bold text-green-600">Positive</p>
                <p className="mt-1 text-3xl font-semibold tabular-nums text-green-600">
                  {positive != null ? `${Number(positive).toFixed(0)}%` : "—"}
                </p>
              </div>

              <div className="rounded-2xl border-2 border-neutral-300 bg-neutral-100 px-4 py-4 shadow-sm">
                <p className="text-sm font-bold text-neutral-900">Neutral</p>
                <p className="mt-1 text-3xl font-semibold tabular-nums text-neutral-900">
                  {neutral != null ? `${Number(neutral).toFixed(0)}%` : "—"}
                </p>
              </div>

              <div className="rounded-2xl border-2 border-red-300 bg-red-100 px-4 py-4 shadow-sm">
                <p className="text-sm font-bold text-red-600">Negative</p>
                <p className="mt-1 text-3xl font-semibold tabular-nums text-red-600">
                  {negative != null ? `${Number(negative).toFixed(0)}%` : "—"}
                </p>
              </div>
            </div>
            <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
              <div className="flex items-center gap-2 mb-3">
                <LuChartBar className="size-4 text-gray-600" />
                <span className="text-sm font-medium text-gray-700">
                  Overall Sentiment Distribution
                </span>
              </div>
              <Bar
                positive={(positive ?? 0) / 100}
                neutral={(neutral ?? 0) / 100}
                negative={(negative ?? 0) / 100}
              />
            </div>
            <div className="space-y-4">
              <h2 className="text-base font-semibold text-neutral-800">
                Top posts ({posts.length})
              </h2>
              {posts.length === 0 ? (
                <p className="text-sm text-neutral-500">
                  {data.source === "db"
                    ? "No top posts stored for this topic yet."
                    : "No posts matched this search."}
                </p>
              ) : (
                posts.map((post, index) => (
                  <div
                    key={post.id != null ? String(post.id) : `post-${index}`}
                    className="rounded-xl border border-neutral-200 bg-white p-4 shadow-sm"
                  >
                    <p className="text-lg font-bold text-neutral-900">
                      Post {index + 1}
                      <span className="ml-2 text-base font-normal text-neutral-500">
                        · {post.platform ?? "unknown"}
                      </span>
                    </p>
                    <p className="mt-2 text-sm font-medium text-neutral-800">
                      @{post.author ?? "unknown"}
                    </p>
                    <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-neutral-700">
                      {post.text}
                    </p>
                    <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-neutral-500">
                      <span
                        className={`rounded-full px-2 py-0.5 font-medium capitalize ${
                          post.label === "positive"
                            ? "bg-green-100 text-green-800"
                            : post.label === "negative"
                              ? "bg-red-100 text-red-800"
                              : "bg-neutral-100 text-neutral-700"
                        }`}
                      >
                        {post.label ?? "—"}
                      </span>
                      {post.compound != null &&
                        !Number.isNaN(Number(post.compound)) && (
                          <span className="tabular-nums">
                            compound {Number(post.compound).toFixed(3)}
                          </span>
                        )}
                      <span className="tabular-nums">
                        {post.like_count ?? 0} likes · {post.repost_count ?? 0}{" "}
                        reposts
                      </span>
                    </div>
                    {post.url && (
                      <a
                        href={post.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="mt-3 inline-block text-sm font-medium text-[var(--color-primary)] underline-offset-2 hover:underline"
                      >
                        View on {post.platform ?? "source"} →
                      </a>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TopicDetailPage;
