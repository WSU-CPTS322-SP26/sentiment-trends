import React from "react";
import styles from "../styles/components/Header.module.css";
import { SearchBar } from "../components/SearchBar";
import { SearchResultsList } from "../components/SearchResultsList";

const Header = ({ title, onSearch, results }) => {
    return (

        <div className={styles.header}>
            <div className={styles.headerContainer}>
                <div className={styles.headerTitleContainer}>
                    <h1 className={styles.headerTitle}>{title}</h1>
                </div>
                <div className={styles.headerSearch}>
                    <SearchBar setResults={onSearch}/>
                    {results?.length > 0 && <SearchResultsList results={results}/>}
                </div>
            </div>
        </div>
    );
}

export default Header;