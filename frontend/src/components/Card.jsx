import styles from "../styles/components/Card.module.css";

const Card = ({title, image, sentiment}) => {
    return (
        <div className={styles.card}>
            <div className={styles.cardHeader}>
                <img className={styles.cardImage}
                src={image}
                alt={title}>
                </img>
                <h2 className={styles.cardTitle}>{title}</h2>
            </div>
            <p className={styles.cardDescription}>{sentiment}</p>
        </div>
    );
}

export default Card;