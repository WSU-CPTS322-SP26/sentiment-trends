import styles from "../styles/components/Card.module.css";
import Bar from "./Bar";

const Card = ({card}) => {
    return (
        <div className={styles.card}>
            <div className={styles.cardHeader}>
                <img className={styles.cardImage}
                src={card.image}
                alt={card.title}>
                </img>
                <h2 className={styles.cardTitle}>{card.title}</h2>
            </div>
            <div className={styles.cardBody}>
                <p>Compound Sentiment: {card.compound_sentiment}</p>
                <Bar negative={card.negative_sentiment} 
                    neutral={card.neutral_sentiment} 
                    positive={card.positive_sentiment} 
                    compound={card.compound_sentiment}
                />
            </div>
        </div>
    );
}

export default Card;