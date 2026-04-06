import { useState } from "react";
import { FiSearch } from "react-icons/fi";
import { useNavigate } from "react-router-dom";
import styles from "../styles/components/SearchBar.module.css";
import { useHomepageCards } from "../utils/HomepageCardsContext";

const SEARCH_RESULTS_LIMIT = 5;

export const SearchBar = ({ setResults }) => {
  const [input, setInput] = useState("");
  const navigate = useNavigate();
  const { cards } = useHomepageCards();

  const fetchData = (value) => {
    const q = value.trim().toLowerCase();
    if (!q) {
      setResults([]);
      return;
    }
    const matches = cards
      .filter((card) => {
        const title = (card.title ?? "").toLowerCase();
        const display = (card.displayTitle ?? "").toLowerCase();
        return title.includes(q) || display.includes(q);
      })
      .slice(0, SEARCH_RESULTS_LIMIT)
      .map((card) => ({
        id: card.id,
        term: card.title,
      }));
    setResults(matches);
  };

  const handleChange = (value) => {
    setInput(value);
    fetchData(value);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && input.trim()) {
      navigate(`/topic/${encodeURIComponent(input.trim())}`);
    }
  };

  return (
    <div className={styles.inputWrapper}>
      <FiSearch className={styles.searchIcon} />
      <input
        className={styles.input}
        placeholder="Type to search..."
        value={input}
        onChange={(e) => handleChange(e.target.value)}
        onKeyDown={handleKeyDown}
      />
    </div>
  );
};
