import { mockCards } from "../../mocks/data/mock_data";
import { useParams } from "react-router-dom";


const CardDetailPage = () => {

const { id } = useParams();
const card = mockCards.find(c => c.id === Number(id));

    if (!card) {
        return <p>Card not found</p>;
    }
    return (
        <div>
            <img src={card.image} alt={card.title} style={{ maxWidth: "300px" }} />
            <h1>{card.title}</h1>
            <b>{card.description}</b>
            <p>Category: {card.category}</p>
            <p>Negative Sentiment: {card.negative_sentiment}</p>
            <p>Neutral Sentiment: {card.neutral_sentiment}</p>
            <p>Positive Sentiment: {card.positive_sentiment}</p>
            <p>Compound Sentiment: {card.compound_sentiment}</p>
            Back to <a href="/">home</a>
        </div>
    );
}
export default CardDetailPage;