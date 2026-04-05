import styles from "../styles/components/Bar.module.css";

/* TODO: Incorporate compound sentiment into bar styling
using some kind of recognizable indicator such as an arrow or bold line */
const Bar = ({ negative, neutral, positive }) => {
  const pPct = Math.round((positive ?? 0) * 100);
  const nPct = Math.round((neutral ?? 0) * 100);
  const nePct = Math.round((negative ?? 0) * 100);

  return (
    <div className={styles.barContainer}>
      <div
        className={styles.barSegment}
        style={{
          width: `${pPct}%`,
          backgroundColor: "var(--color-bar-positive)",
        }}
      >
        {pPct > 0 ? `${pPct}%` : null}
      </div>
      <div
        className={styles.barSegment}
        style={{
          width: `${nPct}%`,
          backgroundColor: "var(--color-bar-neutral)",
        }}
      >
        {nPct > 0 ? `${nPct}%` : null}
      </div>
      <div
        className={styles.barSegment}
        style={{
          width: `${nePct}%`,
          backgroundColor: "var(--color-bar-negative)",
        }}
      >
        {nePct > 0 ? `${nePct}%` : null}
      </div>
    </div>
  );
};

export default Bar;
