import styles from "../styles/components/Bar.module.css";

/* TODO: Incorporate compound sentiment into bar styling
using some kind of recognizable indicator such as an arrow or bold line */
const Bar = ({negative, neutral, positive, compound}) => {
    return (
        <div className={styles.barContainer}>
            <div className={styles.barSegment} style={{width: `${positive * 100}%`, backgroundColor: "var(--color-bar-positive)"}}>{positive * 100}%</div>
            <div className={styles.barSegment} style={{width: `${neutral * 100}%`, backgroundColor: "var(--color-bar-neutral)"}}>{neutral * 100}%</div>
            <div className={styles.barSegment} style={{width: `${negative * 100}%`, backgroundColor: "var(--color-bar-negative)"}}>{negative * 100}%</div>
        </div>
    );
}

export default Bar;