import { useEffect, useMemo, useState } from "react";
import Header from "../components/Header";
import Card from "../components/Card";
import styles from "../styles/pages/HomePage.module.css";
import { appConfig } from "../constants";
import { useSearchParams } from "react-router-dom";
import CardGridSkeleton from "../components/CardGridSkeleton";
import { useHomepageCards } from "../utils/HomepageCardsContext";

const HomePage = () => {
  const PAGE_SIZE = 28;
  const [searchParams] = useSearchParams();
  const catParam = searchParams.get("category");
  const [results, setResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const { cards, loading, error, navbarCategories } = useHomepageCards();

  const filteredCards = useMemo(() => {
    if (!catParam || catParam === "All") return cards;
    return cards.filter((c) => c.category.includes(catParam));
  }, [cards, catParam]);

  const totalPages = Math.max(1, Math.ceil(filteredCards.length / PAGE_SIZE));

  useEffect(() => {
    setCurrentPage(1);
  }, [catParam]);

  useEffect(() => {
    if (currentPage > totalPages) {
      setCurrentPage(totalPages);
    }
  }, [currentPage, totalPages]);

  const paginatedCards = useMemo(() => {
    const start = (currentPage - 1) * PAGE_SIZE;
    return filteredCards.slice(start, start + PAGE_SIZE);
  }, [filteredCards, currentPage]);

  return (
    <div className={styles.HomePage}>
      <Header
        title={appConfig.name}
        onSearch={setResults}
        results={results}
        categories={navbarCategories}
      />
      <div className={styles.pageContainer}>
        {loading && <CardGridSkeleton />}
        {error && <p>Error: {error.message}</p>}
        {!loading && !error && (
          <>
            <div className={styles.cardsContainer}>
              {paginatedCards.map((card) => (
                <Card key={card.id} card={card} />
              ))}
            </div>
            {totalPages > 1 && (
              <nav className={styles.pagination} aria-label="Topic list pagination">
                <button
                  type="button"
                  className={styles.pageButton}
                  onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                  disabled={currentPage === 1}
                >
                  Previous
                </button>
                {Array.from({ length: totalPages }, (_, index) => index + 1).map(
                  (page) => (
                    <button
                      type="button"
                      key={page}
                      className={`${styles.pageButton} ${
                        currentPage === page ? styles.activePage : ""
                      }`}
                      onClick={() => setCurrentPage(page)}
                      aria-current={currentPage === page ? "page" : undefined}
                    >
                      {page}
                    </button>
                  )
                )}
                <button
                  type="button"
                  className={styles.pageButton}
                  onClick={() =>
                    setCurrentPage((p) => Math.min(totalPages, p + 1))
                  }
                  disabled={currentPage === totalPages}
                >
                  Next
                </button>
              </nav>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default HomePage;
