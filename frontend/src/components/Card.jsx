import styles from "../styles/components/Card.module.css";
import Bar from "./Bar";

const Card = ({title, image, negative_sentiment, neutral_sentiment, positive_sentiment, compound_sentiment}) => {
    return (
        <div className={styles.card}>
            <div className={styles.cardHeader}>
                <img className={styles.cardImage}
                src={image}
                alt={title}>
                </img>
                <h2 className={styles.cardTitle}>{title}</h2>
            </div>
            <div className={styles.cardBody}>
                <p>Compound Sentiment: {compound_sentiment}</p>
                <Bar negative={negative_sentiment} 
                    neutral={neutral_sentiment} 
                    positive={positive_sentiment} 
                    compound={compound_sentiment}
                />
            </div>
        </div>
    );
}

export default Card;