import styles from "../styles/components/Card.module.css";
import Bar from "./Bar";
import { Link } from "react-router-dom";

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

const Card = ({ card }) => {
  const titleForUrl = encodeURIComponent(card.title);
  const heading = card.displayTitle ?? card.title;
  const phrase = sentimentPhrase(
    card.positive_sentiment,
    card.neutral_sentiment,
    card.negative_sentiment
  );

  return (
    <div className={styles.card}>
      <Link to={`/topic/${titleForUrl}`} className={styles.cardHeader}>
        <img
          className={styles.cardImage}
          src={card.image}
          alt={heading}
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
      </div>
    </div>
  );
};

export default Card;
