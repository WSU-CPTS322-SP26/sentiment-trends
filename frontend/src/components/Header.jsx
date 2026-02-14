import React from "react";
import styles from "../styles/components/Header.module.css";
import { SearchBar } from "../components/SearchBar";
import { SearchResultsList } from "../components/SearchResultsList";

const Header = ({ title, onSearch, results }) => {
    return (
        <div className={styles.header}>
            <div className={styles.headerRow}>
                <h2>{title}</h2>
                <div className={styles.searchBarContainer}>
                    <SearchBar setResults={onSearch}/>
                </div>
            </div>
            <SearchResultsList results={results}/>
        </div>
    );
}

export default Header;