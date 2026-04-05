import { Link } from "react-router-dom";
import styles from "../styles/components/SearchResult.module.css";

export const SearchResult = ({ result }) => {
  const to = `/topic/${encodeURIComponent(result.term.trim())}`;
  return (
    <Link to={to} className={styles.searchResult}>
      {result.term}
    </Link>
  );
};