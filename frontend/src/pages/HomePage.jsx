import { useEffect, useMemo, useState } from "react";
import Header from "../components/Header";
import Card from "../components/Card";
import styles from "../styles/pages/HomePage.module.css";
import { appConfig } from "../constants";
import { api } from "../services/api";
import { useSearchParams } from "react-router-dom";
import topicPlaceholder from "../assets/topic-placeholder.svg";

// title-style casing for display (routing still uses raw api title)
function toTitleCase(name) {
  if (!name || typeof name !== "string") return name;
  return name.replace(/\w[\w'-]*/g, (w) => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase());
}

// all first, then only category labels that appear on at least one card
function categoriesFromCards(cards) {
  const nav = [{ id: "all", label: "All", href: "/" }];
  const seen = new Set();
  for (const c of cards) {
    for (const lab of c.category) {
      if (lab && typeof lab === "string") seen.add(lab);
    }
  }
  const sorted = [...seen].sort((a, b) => a.localeCompare(b));
  for (const label of sorted) {
    nav.push({
      id: label,
      label,
      href: `/?category=${encodeURIComponent(label)}`,
    });
  }
  return nav;
}

function mapApiCardToDisplay(api) {
  const pos = api.positive_pct;
  const neu = api.neutral_pct;
  const neg = api.negative_pct;
  const rawCat = api.category;
  const category = Array.isArray(rawCat)
    ? rawCat
    : rawCat
      ? [rawCat]
      : [];
  return {
    id: api.id,
    title: api.title,
    displayTitle: toTitleCase(api.title),
    image: topicPlaceholder,
    category,
    positive_sentiment: (pos ?? 0) / 100,
    neutral_sentiment: (neu ?? 0) / 100,
    negative_sentiment: (neg ?? 0) / 100,
  };
}

const HomePage = () => {
  const [searchParams] = useSearchParams();
  const catParam = searchParams.get("category");
  const [results, setResults] = useState([]);
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    api
      .getHomepageCards()
      .then((data) => {
        const raw = data?.cards;
        setCards(
          Array.isArray(raw) ? raw.map((c) => mapApiCardToDisplay(c)) : []
        );
      })
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  const navbarCategories = useMemo(() => categoriesFromCards(cards), [cards]);

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
        {loading && <p>Loading...</p>}
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
