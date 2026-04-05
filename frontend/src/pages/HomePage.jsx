import { useMemo, useState } from "react";
import Header from "../components/Header";
import Card from "../components/Card";
import styles from "../styles/pages/HomePage.module.css";
import { appConfig } from "../constants";
import { useSearchParams } from "react-router-dom";
import Loader from "../components/Loader";
import { useHomepageCards } from "../utils/HomepageCardsContext";

const HomePage = () => {
  const [searchParams] = useSearchParams();
  const catParam = searchParams.get("category");
  const [results, setResults] = useState([]);
  const { cards, loading, error, navbarCategories } = useHomepageCards();

  const filteredCards = useMemo(() => {
    if (!catParam || catParam === "All") return cards;
    return cards.filter((c) => c.category.includes(catParam));
  }, [cards, catParam]);

  return (
    <div className={styles.HomePage}>
      <Header
        title={appConfig.name}
        onSearch={setResults}
        results={results}
        categories={navbarCategories}
      />
      <div className={styles.pageContainer}>
        {loading && <Loader />}
        {error && <p>Error: {error.message}</p>}
        {!loading && !error && (
          <div className={styles.cardsContainer}>
            {filteredCards.map((card) => (
              <Card key={card.id} card={card} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
