import React from 'react'
import { SearchResult } from "./SearchResult";
import styles from "../styles/components/SearchResultsList.module.css";

export const SearchResultsList = ({ results }) => {
    return (
    <div className={styles.searchResultsList}>
    {
        results.map((result) => {
            return  <SearchResult result={result} key={result.id}/>;
        })
    }
    </div>
    );
}