import React from 'react'
import styles from "../styles/components/SearchResult.module.css";

export const SearchResult = ({ result }) => {
    return (<div className={styles.searchResult} onClick={(e) => alert(`${result.term}`)}
    >{result.term}</div>);
}