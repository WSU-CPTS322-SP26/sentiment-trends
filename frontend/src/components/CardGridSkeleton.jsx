import homeStyles from "../styles/pages/HomePage.module.css";
import cardStyles from "../styles/components/Card.module.css";

const PLACEHOLDER_COUNT = 20;

function CardSkeletonItem() {
  return (
    <div className={`${cardStyles.card} w-full min-w-0`} aria-hidden>
      <div className={cardStyles.cardHeader}>
        <div
          className={`${cardStyles.cardImage} shrink-0 bg-neutral-200 animate-pulse`}
        />
        <div className="ml-3 flex min-w-0 flex-1 flex-col gap-2">
          <div className="h-5 max-w-[85%] rounded-md bg-neutral-200 animate-pulse" />
          <div className="h-4 max-w-[55%] rounded-md bg-neutral-200 animate-pulse" />
        </div>
      </div>
      <div className={cardStyles.cardBody}>
        <div className="h-4 w-40 rounded-md bg-neutral-200 animate-pulse" />
        <div className="h-8 w-full max-w-[280px] rounded-md bg-neutral-200 animate-pulse" />
      </div>
    </div>
  );
}

const CardGridSkeleton = () => {
  return (
    <div
      className={homeStyles.cardsContainer}
      aria-busy="true"
      aria-label="Loading topics"
    >
      {Array.from({ length: PLACEHOLDER_COUNT }, (_, i) => (
        <CardSkeletonItem key={i} />
      ))}
    </div>
  );
};

export default CardGridSkeleton;
