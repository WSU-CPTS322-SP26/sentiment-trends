import styles from "../styles/components/Card.module.css";
import Bar from "./Bar";
import { Link } from "react-router-dom";

const Card = ({card}) => {
    return (
        <div className={styles.card}>
            <Link to={`/card/${card.id}`} className={styles.cardHeader}>
                <img className={styles.cardImage}
                src={card.image}
                alt={card.title}>
                </img>
                <h2 className={styles.cardTitle}>{card.title}</h2>
            </Link>
            <div className={styles.cardBody}>
                <p> 
                    <strong>
                        {card.compound_sentiment * 100}%
                    </strong> 
                    {
                    card.compound_sentiment < 0.5 && card.compound_sentiment > 0.1 ? " Slightly Positive" :
                    card.compound_sentiment > 0.1 ? " Overwhelmingly Positive" :
                    card.compound_sentiment < -0.1 && card.compound_sentiment > -0.5 ? " Slightly Negative" :
                    card.compound_sentiment < -0.1 ? " Overwhelmingly Negative" :
                    " Neutral"
                }</p>
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