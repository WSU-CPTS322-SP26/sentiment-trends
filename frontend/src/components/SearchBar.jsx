import { useState } from 'react';
import { FiSearch } from "react-icons/fi";
import { mockSearch } from '../../mock_data/mock_data';
import styles from "../styles/components/SearchBar.module.css";

export const SearchBar = ({ setResults }) => {
  const [input, setInput] = useState("");

  const fetchData = (value) => {
    const results = mockSearch.filter((search) => {
      return (
        value &&
        search &&
        search.term && 
        search.term.toLowerCase().includes(value.toLowerCase())
      );
    });
    setResults(results);
  };

  const handleChange = (value) => {
    setInput(value);
    fetchData(value);
  };

    return (
      <div className={styles.inputWrapper}>
        <FiSearch className={styles.searchIcon} />
        <input 
          className={styles.input}
          placeholder="Type to search..." 
          value={input}
          onChange={(e) => handleChange(e.target.value)}
        />
      </div>
    );
};