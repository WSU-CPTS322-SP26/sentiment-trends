import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "../services/api";
import styles from "../styles/pages/TopicDetailPage.module.css";
import Header from "../components/Header";
import { appConfig } from "../constants";
import Bar from "../components/Bar";
import { LuChartBar } from "react-icons/lu";
import TopicDetailPageSkeleton from "../components/TopicDetailPageSkeleton";
import { toTitleCase } from "../utils/helpers";
import { useHomepageCards } from "../utils/HomepageCardsContext";
import { overallToneLabel } from "../utils/sentimentTone";

const TopicDetailPage = ({ theme, onToggleTheme }) => {
  const { topic: topicParam } = useParams();
  const { navbarCategories } = useHomepageCards();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [results, setResults] = useState([]);

  const [summary, setSummary] = useState(null);
  const [summaryLoading, setSummaryLoading] = useState(false);
  const [summaryError, setSummaryError] = useState(null);

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
    setSummary(null);
    setSummaryLoading(false);
    setSummaryError(null);

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
          setSummary(fromDb?.topic?.summary ?? null);
          return;
        }
        const live = await api.getSentimentAnalysis(topicSlug, 25, 5);
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

  const handleGenerateSummary = async () => {
    try {
      setSummaryLoading(true);
      setSummaryError(null);
      const res = await api.getOllamaSummary(topicSlug, 25, 5);
      setSummary(res?.summary ?? null);
    } catch (e) {
      setSummaryError(e);
    } finally {
      setSummaryLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={styles.DetailPage}>
        <Header
          title={appConfig.name}
          onSearch={setResults}
          results={results}
          categories={navbarCategories}
          theme={theme}
          onToggleTheme={onToggleTheme}
        />
        <div className={`${styles.pageContainer} min-h-screen`}>
          <div className={`${styles.content} py-4`}>
            <div className={`${styles.panel} ${styles.sectionCard} space-y-4`}>
              <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
                Sentiment Analysis: {toTitleCase(topicSlug)}
              </h1>
              <TopicDetailPageSkeleton />
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
          theme={theme}
          onToggleTheme={onToggleTheme}
        />
        <div className={`${styles.pageContainer} min-h-screen`}>
          <div className={`${styles.content} py-4`}>
            <div className={`${styles.panel} ${styles.sectionCard} space-y-4`}>
              <h1 className="text-3xl font-bold text-[var(--color-text-primary)]">
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
  const overallTone = overallToneLabel(compound, positive, negative);

  function sentimentColor(value) {
    if (value == null || Number.isNaN(value)) return "text-neutral-400";
    if (value > -0.05 && value < 0.05) return "text-neutral-700";
    if (value < 0) return "text-red-600";
    return "text-green-600";
  }

  return (
    <div className={styles.DetailPage}>
      <Header
        title={appConfig.name}
        onSearch={setResults}
        results={results}
        categories={navbarCategories}
        theme={theme}
        onToggleTheme={onToggleTheme}
      />
      <div className={`${styles.pageContainer} min-h-screen`}>
        <div className={`${styles.content} py-4`}>
          <div className={`${styles.panel} ${styles.sectionCard} space-y-3`}>
            <h1 className="text-3xl font-bold text-[var(--color-text-primary)] leading-tight">
              Sentiment Analysis: {toTitleCase(displayTitle)}
            </h1>
            {data.source === "live" && (
              <p className="text-sm text-amber-800 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2">
                Live analysis: results are fetched on demand and not from the
                database
              </p>
            )}
            {data.source === "db" && snapshotAt && (
              <p className="text-sm text-[var(--color-text-secondary)] leading-tight -mt-1">
                {new Date(snapshotAt).toLocaleString()}
              </p>
            )}

            <div className="rounded-2xl border-2 border-[var(--color-border-muted)] bg-[var(--color-score-tint)] px-4 py-3 shadow-sm">
              <p className="text-sm font-bold text-[var(--color-text-secondary)] leading-tight">
                Overall tone
              </p>
              <p
                className={`mt-0.5 text-3xl font-semibold leading-tight ${sentimentColor(compound)}`}
              >
                {overallTone ?? "—"}
              </p>
              {compound != null && (
                <p className="mt-1.5 text-xs text-[var(--color-text-secondary)] leading-snug">
                  Based on a compound score of{" "}
                  <span className="font-medium tabular-nums text-[var(--color-text-primary)]">
                    {compound.toFixed(3)}
                  </span>{" "}
                  (from -1, most negative, to +1, most positive).
                </p>
              )}
            </div>

            <div className="rounded-xl p-4 border border-[var(--color-border-muted)] bg-[var(--color-elevated-2)]">
              <div className="flex items-center gap-2 mb-3">
                <LuChartBar className="size-4 text-[var(--color-text-secondary)]" />
                <span className="text-sm font-medium text-[var(--color-text-secondary)]">
                  Overall Sentiment Distribution
                </span>
              </div>
              <Bar
                positive={(positive ?? 0) / 100}
                neutral={(neutral ?? 0) / 100}
                negative={(negative ?? 0) / 100}
              />
            </div>
            
            <div className="rounded-2xl border-2 border-[var(--color-border-muted)] bg-[var(--color-elevated)] px-6 py-5 shadow-sm space-y-3">
              <h2 className="text-lg font-semibold text-[var(--color-text-primary)]">Topic Summary</h2>

              {summary ? (
                <p className="text-sm leading-relaxed text-[var(--color-text-secondary)] whitespace-pre-wrap">
                  {summary}
                </p>
              ) : (
                <>
                  <p className="text-sm text-[var(--color-text-secondary)]">
                    No stored summary available for this topic yet.
                  </p>
                  <button
                    type="button"
                    onClick={handleGenerateSummary}
                    disabled={summaryLoading}
                    className="inline-flex items-center rounded-lg border border-[var(--color-border-muted)] px-3 py-2 text-sm font-medium text-[var(--color-text-primary)] hover:bg-[var(--color-elevated-2)] disabled:opacity-60"
                  >
                    {summaryLoading ? "Generating..." : "Generate Summary"}
                  </button>
                  {summaryError && (
                    <p className="text-sm text-red-600" role="alert">
                      {summaryError.message}
                    </p>
                  )}
                </>
              )}
            </div>

            <div className="space-y-4">
              <h2 className="text-base font-semibold text-[var(--color-text-primary)]">
                Top posts ({posts.length})
              </h2>
              {posts.length === 0 ? (
                <p className="text-sm text-[var(--color-text-secondary)]">
                  {data.source === "db"
                    ? "No top posts stored for this topic yet."
                    : "No posts matched this search."}
                </p>
              ) : (
                posts.map((post, index) => (
                  <div
                    key={post.id != null ? String(post.id) : `post-${index}`}
                    className="rounded-xl border border-[var(--color-border-muted)] bg-[var(--color-elevated)] p-4 shadow-sm"
                  >
                    <p className="text-lg font-bold text-[var(--color-text-primary)]">
                      Post {index + 1}
                      <span className="ml-2 text-base font-normal text-[var(--color-text-secondary)]">
                        · {post.platform ?? "unknown"}
                      </span>
                    </p>
                    <p className="mt-2 text-sm font-medium text-[var(--color-text-primary)]">
                      @{post.author ?? "unknown"}
                    </p>
                    <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-[var(--color-text-secondary)]">
                      {post.text}
                    </p>
                    <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-[var(--color-text-secondary)]">
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
