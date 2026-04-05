import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";
import { api } from "../services/api";
import { categoriesFromCards, mapApiCardToDisplay } from "../utils/helpers";

const HomepageCardsContext = createContext(null);

export function HomepageCardsProvider({ children }) {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const navbarCategories = useMemo(
    () => categoriesFromCards(cards),
    [cards]
  );

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

  const value = useMemo(
    () => ({
      cards,
      loading,
      error,
      navbarCategories,
    }),
    [cards, loading, error, navbarCategories]
  );

  return (
    <HomepageCardsContext.Provider value={value}>
      {children}
    </HomepageCardsContext.Provider>
  );
}

export function useHomepageCards() {
  const ctx = useContext(HomepageCardsContext);
  if (!ctx) {
    throw new Error(
      "useHomepageCards must be used within HomepageCardsProvider"
    );
  }
  return ctx;
}