import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import topicPlaceholder from "../assets/topic-placeholder.svg";
import styles from "../styles/components/Card.module.css";
import Bar from "./Bar";

// same rounded shares as the bar; ties → mixed
function sentimentPhrase(positive, neutral, negative) {
  const p = Math.round((positive ?? 0) * 100);
  const n = Math.round((neutral ?? 0) * 100);
  const ne = Math.round((negative ?? 0) * 100);
  if (p + n + ne === 0) return "No data";
  const buckets = [
    { key: "positive", v: p },
    { key: "neutral", v: n },
    { key: "negative", v: ne },
  ];
  const maxV = Math.max(p, n, ne);
  const winners = buckets.filter((b) => b.v === maxV && b.v > 0);
  if (winners.length !== 1) return "Mixed sentiment";
  if (winners[0].key === "positive") return "Mostly positive";
  if (winners[0].key === "neutral") return "Mostly neutral";
  return "Mostly negative";
}

function compactNumber(value) {
  if (typeof value !== "number" || Number.isNaN(value)) return "N/A";
  return new Intl.NumberFormat("en-US", {
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

const Card = ({ card }) => {
  const titleForUrl = encodeURIComponent(card.title);
  const heading = card.displayTitle ?? card.title;
  const phrase = sentimentPhrase(
    card.positive_sentiment,
    card.neutral_sentiment,
    card.negative_sentiment,
  );

  const [imageSrc, setImageSrc] = useState(card.image);
  useEffect(() => {
    setImageSrc(card.image);
  }, [card.image]);

  const onImageError = () => {
    setImageSrc((prev) =>
      prev === topicPlaceholder ? prev : topicPlaceholder,
    );
  };
  const increaseText =
    typeof card.increase_pct === "number" && Number.isFinite(card.increase_pct)
      ? `+${card.increase_pct}%`
      : "—";
  const searchesText =
    typeof card.searches === "number" && Number.isFinite(card.searches)
      ? `${compactNumber(card.searches)} searches`
      : "—";

  return (
    <div className={styles.card}>
      <Link to={`/topic/${titleForUrl}`} className={styles.cardHeader}>
        <img
          className={styles.cardImage}
          src={imageSrc}
          alt={heading}
          referrerPolicy="no-referrer"
          loading="lazy"
          onError={onImageError}
        />
        <h2 className={styles.cardTitle}>{heading}</h2>
      </Link>
      <div className={styles.cardBody}>
        <p className={styles.sentimentSummary}>
          <strong className={styles.sentimentPhrase}>{phrase}</strong>
        </p>
        <Bar
          negative={card.negative_sentiment}
          neutral={card.neutral_sentiment}
          positive={card.positive_sentiment}
        />
        <div className={styles.subData}>
          <span className={styles.subDataItem}>{searchesText}</span>
          <span className={styles.subDataItem}>{increaseText}</span>
        </div>
      </div>
    </div>
  );
};

export default Card;
