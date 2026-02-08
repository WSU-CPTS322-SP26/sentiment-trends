import React, { useState } from 'react';
import { FaSearch } from "react-icons/fa";
import { mockSearch } from '../../mock_data/mock_data';
import "./SearchBar.css";

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
      <div className="input-wrapper">
        <FaSearch id="search-icon" />
        <input placeholder="Type to search..." 
        value={input}
        onChange={(e) => handleChange(e.target.value)}
        />
      </div>
    );
};