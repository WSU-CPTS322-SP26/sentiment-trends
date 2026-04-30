import styles from "../styles/components/Card.module.css";

const CardSkeleton = () => (
  <div className={styles.card} aria-hidden>
    <div className={styles.cardHeader}>
      <div className={`${styles.cardImage} bg-[var(--color-skeleton-base)] animate-pulse`} />
      <div className="ml-2 h-5 min-w-0 flex-1 rounded bg-[var(--color-skeleton-base)] animate-pulse" />
    </div>
    <div className={styles.cardBody}>
      <div className="h-4 w-32 rounded bg-[var(--color-skeleton-base)] animate-pulse" />
      <div className="h-8 w-full max-w-[200px] rounded bg-[var(--color-skeleton-strong)] animate-pulse" />
    </div>
  </div>
);

export default CardSkeleton;
